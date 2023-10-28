# main.py

import requests
from icalendar import Calendar
from get_calendar_service import get_calendar_service


color_assignments = {}  # Global dictionary to track color assignments

def main():
    ical_url = "https://cloud.timeedit.net/chalmers/web/public/ri6YZ438Xy5Z7gQ5Y86005Z15n0563Y0u076XQ8Qv276wZQ4Qn5660.ics" 
    ical_data = fetch_ical_data(ical_url)

    index = 0
    for event in ical_data.walk('vevent'):

        event = extract_activity_from_description(event)
        event = modify_event_summary(event)
        event = modify_event_description(event)
        event = set_event_color_based_on_activity(event)

        if index == 5 or index == 6 or index == 7:
            calendar_id = "4f24358368de9c1e26ec87f059007df9fc41831dab201f1af638e07d45d88215@group.calendar.google.com" # <YOUR_TARGET_CALENDAR_ID>
            create_google_calendar_event(event, calendar_id)
        index += 1
        print_event(event)

        

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




# Fetch iCalendar data from the URL
def fetch_ical_data(ical_url):
    response = requests.get(ical_url)
    return Calendar.from_ical(response.text)




# Create a Google Calendar event from an iCalendar event
def create_google_calendar_event(event, calendar_id='primary'):
    service = get_calendar_service()

    google_event = {
        'summary': event.get('summary'),
        'location': event.get('location'),
        'description': event.get('description'),
        'start': {
            'dateTime': event.get('dtstart').dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Europe/Stockholm', # YOUR_TIME_ZONE
        },
        'end': {
            'dateTime': event.get('dtend').dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Europe/Stockholm',
        },
    }
        
    # Add colorId if it exists in the event
    if 'colorId' in event:
        google_event['colorId'] = event['colorId']

    created_event = service.events().insert(calendarId=calendar_id, body=google_event).execute()
    print(f"Event created: {created_event['htmlLink']}")




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
    # start = event['start'].get('dateTime', event['start'].get('date'))
    # print(start, event['summary'])


if __name__ == "__main__":
    main()