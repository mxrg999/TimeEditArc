# CalendarManager.py

import datetime
import pytz
from src.get_calendar_service import get_calendar_service
from dateutil.parser import parse

class CalendarManager:
    def __init__(self, config):
        self.config = config
        self.service = get_calendar_service()

    # Find an existing event with the same summary and start time
    def find_existing_event(self, calendar_id, summary, start_time):
        # Check if self.service is initialized
        if self.service is None:
            print("Error: Google Calendar service is not initialized.")
            return None
        
        # Convert start_time to RFC3339 format which Google Calendar API uses
        start_time_rfc = start_time.strftime('%Y-%m-%dT%H:%M:%S%z')

        # Get the end of the day for the given start_time
        end_time = start_time.replace(hour=23, minute=59, second=59)
        end_time_rfc = end_time.strftime('%Y-%m-%dT%H:%M:%S%z')

        events_result = self.service.events().list(calendarId=calendar_id, 
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

            if event_start_time_utc == start_time_utc:
                return event

        # If no exact match found, return None
        return None

    # Create or update a Google Calendar event
    def create_or_update_event(self, event, only_update_existing_events):
        # If the event is an all-day event (i.e., it's a date object and not a datetime object), skip it
        if isinstance(event.get('dtstart').dt, datetime.date) and not isinstance(event.get('dtstart').dt, datetime.datetime):
            print(f"Skipping all-day event: {event.get('summary')}")
            return

        google_event = {
            'summary': event.get('summary'),
            'location': event.get('location'),
            'description': event.get('description'),
            'start': {
                'dateTime': event.get('dtstart').dt.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': self.config['time_zone']
            },
            'end': {
                'dateTime': event.get('dtend').dt.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': self.config['time_zone']
            },
        }

        # Add colorId if it exists in the event
        if 'colorId' in event:
            google_event['colorId'] = event['colorId']
        print(f"Checking for event: {google_event['summary']} at {event.get('dtstart').dt}")

        # Check if an event with the same summary and start time already exists
        existing_event = self.find_existing_event(self.config['calendar_id'], google_event['summary'], event.get('dtstart').dt)

        if existing_event:
            # Update the event
            updated_event = self.service.events().update(calendarId=self.config['calendar_id'], eventId=existing_event['id'], body=google_event).execute()
            print(f"Event updated. ID: {updated_event['id']}")
            self.print_event(event)
        elif not only_update_existing_events:
            # Insert a new event
            created_event = self.service.events().insert(calendarId=self.config['calendar_id'], body=google_event).execute()
            print("No existing event found.")
            print(f"Event created. ID: {created_event['id']}")
        else:
            # No existing event found and only_update_existing_events is True
            print("No existing event found. Skipping...")

    # Print the event's details
    def print_event(self, event):
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