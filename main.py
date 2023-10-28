# main.py

import requests
from icalendar import Calendar
from get_calendar_service import get_calendar_service


def main():
    ical_url =  "<YOUR_ICAL_URL>"
    ical_data = fetch_ical_data(ical_url)

    for event in ical_data.walk('vevent'):
        calendar_id = "<YOUR_TARGET_CALENDAR_ID>"
        create_google_calendar_event(event, calendar_id)
        print_event(event)

        
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
        'colorId': '11', # Color: Tomato
        'start': {
            'dateTime': event.get('dtstart').dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Europe/Stockholm', # YOUR_TIME_ZONE
        },
        'end': {
            'dateTime': event.get('dtend').dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Europe/Stockholm',
        },
    }
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


if __name__ == "__main__":
    main()