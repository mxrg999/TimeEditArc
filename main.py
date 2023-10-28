# main.py
"""
    Fetches iCalendar data from a URL, modifies the data, and creates or updates events on a Google Calendar.
    The modified data includes extracted course codes and names, activity types, and assigned colors based on course and activity.
    The script uses the Google Calendar API to create or update events on a target Google Calendar.

    Created and maintained by @mxrg999
"""

import requests
import pytz
import argparse
import configparser

from icalendar import Calendar
import datetime
from dateutil.parser import parse

from get_calendar_service import get_calendar_service


color_assignments = {}  # Global dictionary to track color assignments

def main():       
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="TimeEditArc - Import your TimeEdit schedule to Google Calendar")
    parser.add_argument('--env', type=str, default='DEFAULT', help='Environment to use (e.g., development)')
    args = parser.parse_args()

    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    environment = args.env

    print(f"Script is running on '{environment}' environment.")

    try:
        calendar_id = config[environment]['calendar_id']
        ical_url = config[environment]['ical_url']
    except KeyError:
        print(f"Error: Configuration not found for environment '{environment}' in config.ini")
        exit(1)
    
    ical_data = fetch_ical_data(ical_url)
    for event in ical_data.walk('vevent'):
        event = extract_activity_from_description(event)
        event = modify_event_summary(event)
        event = modify_event_description(event)
        event = set_event_color_based_on_activity(event)
        create_or_update_google_calendar_event(event, calendar_id)
        print_event(event)

    print("Your calendar has now been imported/updated.")

# Fetch iCalendar data from the URL
def fetch_ical_data(ical_url):
    response = requests.get(ical_url)
    return Calendar.from_ical(response.text)
        

# Modify the event's summary
def modify_event_summary(event):
    summary = event.get('summary')
    course_parts = summary.split(", ")
    
    # Extract the first course code and its corresponding name
    if '. Course name: ' in course_parts[0]:
        course_code, course_name = course_parts[0].split('. Course name: ')
        
        # Add the extracted course code and name to the event object
        event['course_code'] = course_code  
        event['course_name'] = course_name

        # Create a new summary based on the extracted course code and name
        new_summary = f"{course_name} - {course_code}"
        
        # Add the activity type to the summary if it exists
        activity_type = event.get('activity', None)
        if activity_type: 
            new_summary = f"{course_name} - {activity_type} - {course_code}"
        else:
            new_summary = f"{course_name} - {course_code}"
    else: # Use the first part as-is if it doesn't match the expected format
        new_summary = course_parts[0]  
    
    # Update the event's summary
    event['summary'] = new_summary

    return event


# Modify the event's description
def modify_event_description(event):
    description = event.get('description')
    new_description = description
    
    activity_type = event.get('activity', None)
    if activity_type:
        new_description = f"{activity_type}"

    event['description'] = new_description
    return event


# Set the event's color based on the activity type
def set_event_color_based_on_activity(event):
    global color_assignments

    course_code = event.get('course_code')
    activity = event.get('activity')

    # If this combination of course_code and activity has been seen before, use the assigned color
    if (course_code, activity) in color_assignments:
        event['colorId'] = color_assignments[(course_code, activity)]
        return event

    # If this combination is new, assign a new color
    available_colors = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    for color in available_colors:
        if color not in color_assignments.values():
            event['colorId'] = color
            color_assignments[(course_code, activity)] = color
            break

    return event


# Extract the activity type from the event's description
def extract_activity_from_description(event):
    description = event.get('description')
    
    # Look for the "Aktivitet: " field in the description
    activity_prefix = "Aktivitet: "
    if activity_prefix in description:
        # Split the description based on the activity prefix and take the second part
        # Taking the first word after "Aktivitet: "
        activity = description.split(activity_prefix)[1].strip().split()[0]  
        
        # Check if the activity is one of the expected types
        if activity in ["Laboration", "Exercise", "Lecture"]:
            event['activity'] = activity  # Add the extracted activity to the event object

    # Return the modified event object
    return event


# Find an existing event with the same summary and start time
def find_existing_event(service, calendar_id, summary, start_time):
    # Convert start_time to RFC3339 format which Google Calendar API uses
    start_time_rfc = start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    
    # Get the end of the day for the given start_time
    end_time = start_time.replace(hour=23, minute=59, second=59)
    end_time_rfc = end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    
    events_result = service.events().list(calendarId=calendar_id, 
                                          q=summary,  # search query
                                          timeMin=start_time_rfc, 
                                          timeMax=end_time_rfc,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    print(f"Found {len(events)} events for the given day.")
    
    # Iterate through each event and find the exact match
    for event in events: 
        event_start_time_utc = parse(event['start'].get('dateTime')).astimezone(pytz.utc)
        start_time_utc = parse(start_time_rfc).astimezone(pytz.utc)

        if event_start_time_utc == start_time_utc and event['summary'] == summary:
            return event

    # If no exact match found, return None
    return None


# Create or update a Google Calendar event
def create_or_update_google_calendar_event(event, calendar_id='primary'):

    # If the event is an all-day event (i.e., it's a date object and not a datetime object), skip it
    if isinstance(event.get('dtstart').dt, datetime.date) and not isinstance(event.get('dtstart').dt, datetime.datetime):
        print(f"Skipping all-day event: {event.get('summary')}")
        return

    service = get_calendar_service()
    
    google_event = {
        'summary': event.get('summary'),
        'location': event.get('location'),
        'description': event.get('description'),
        'start': {
            'dateTime': event.get('dtstart').dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Etc/GMT', # YOUR_TIME_ZONE 'timeZone': 'Europe/Stockholm'
        },
        'end': {
            'dateTime': event.get('dtend').dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Etc/GMT',
        },
    }
        
    # Add colorId if it exists in the event
    if 'colorId' in event:
        google_event['colorId'] = event['colorId']
    print(f"Checking for event: {google_event['summary']} at {event.get('dtstart').dt}")

    # Check if an event with the same summary and start time already exists
    existing_event = find_existing_event(service, calendar_id, google_event['summary'], event.get('dtstart').dt)

    if existing_event:
        # Update the event
        updated_event = service.events().update(calendarId=calendar_id, eventId=existing_event['id'], body=google_event).execute()
        print(f"Found existing event with ID: {existing_event['id']}")
        print(f"Event updated: {updated_event['htmlLink']}")
        
    else:
        # Insert a new event
        created_event = service.events().insert(calendarId=calendar_id, body=google_event).execute()
        print(f"Event created: {created_event['htmlLink']}")
        print("No existing event found.")


# Print the event's details
def print_event(event):
    summary = event.get('summary')
    dtstart = event.get('dtstart').dt
    dtend = event.get('dtend').dt
    location = event.get('location')
    description = event.get('description')
    organizer = event.get('organizer')
    print(f"summary: {summary}")
    print(f"dtstart: {dtstart}")
    print(f"dtend: {dtend}")
    print(f"location: {location}")
    print(f"description: {description}")
    print(f"organizer: {organizer}")
    print("-" * 40)


if __name__ == "__main__":
    main()