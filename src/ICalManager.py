# ICalManager.py

import requests
from icalendar import Calendar

class ICalManager:
    def __init__(self, config):
        self.config = config
        self.color_assignments = {}

    def run(self):
        ical_data = self.fetch_ical_data()
        self.modify_ical_data(ical_data)
        return ical_data

    def modify_ical_data(self, ical_data):
        for event in ical_data.walk('vevent'):
            event = self.extract_activity_from_description(event)
            event = self.modify_event_summary(event)
            event = self.modify_event_description(event)
            event = self.set_event_color_based_on_activity(event)

    def fetch_ical_data(self):
        response = requests.get(self.config['ical_url'])
        return Calendar.from_ical(response.text)

    def modify_event_summary(self, event):
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

    def modify_event_description(self, event):
        description = event.get('description')
        new_description = description

        activity_type = event.get('activity', None)
        if activity_type:
            new_description = f"{activity_type}"

        event['description'] = new_description
        return event

    def set_event_color_based_on_activity(self, event):
        self.color_assignments

        course_code = event.get('course_code')
        activity = event.get('activity')

        # If this combination of course_code and activity has been seen before, use the assigned color
        if (course_code, activity) in self.color_assignments:
            event['colorId'] = self.color_assignments[(course_code, activity)]
            return event

        # If this combination is new, assign a new color
        available_colors = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
        for color in available_colors:
            if color not in self.color_assignments.values():
                event['colorId'] = color
                self.color_assignments[(course_code, activity)] = color
                break

        return event

    def extract_activity_from_description(self, event):
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