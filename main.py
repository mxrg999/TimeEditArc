# main.py
"""
    Fetches iCalendar data from a URL, modifies the data, and creates or updates events on a Google Calendar.
    The modified data includes extracted course codes and names, activity types, and assigned colors based on course and activity.
    The script uses the Google Calendar API to create or update events on a target Google Calendar.

    Created and maintained by @mxrg999
"""

from CalendarManager import CalendarManager
from ConfigManager import ConfigManager
from ICalManager import ICalManager

def main():
    config_manager = ConfigManager()
    config = None
    
    while True:
        choice = input("Choose an option: \
                       \n1. Set up a new configuration \
                       \n2. Load an existing configuration \
                       \n3. Remove a profile \
                       \n4. Rename a profile \
                       \n5. Process and update calendar \
                       \nEnter your choice (1/2/3/4/5): ")
        
        if choice in ['1', '2']:
            config = config_manager.setup_configuration() if choice == '1' else config_manager.load_configuration()
            ical_manager = ICalManager(config)
            calendar_manager = CalendarManager(config)
        elif choice == '3':
            config_manager.remove_profile()
            continue
        elif choice == '4':
            config_manager.rename_profile()
            continue
        elif choice == '5':
            if not config:
                print("Configuration not loaded!")
                load_choice = input("Would you like to load an existing configuration? (yes/no): ").lower()
                if load_choice == 'yes':
                    config = config_manager.load_configuration()
                    if not config:  # If they failed or canceled loading the config
                        continue
                    ical_manager = ICalManager(config)
                    calendar_manager = CalendarManager(config)
                else:
                    print("Please load or set up a configuration first.")
                    continue

            ical_manager = ICalManager(config)
            ical_data = ical_manager.run()
            
            calendar_manager = CalendarManager(config)
            for event in ical_data.walk('vevent'):
                ...
                calendar_manager.create_or_update_event(event)
                calendar_manager.print_event(event)
            
            print("Your calendar has now been imported/updated.")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

if __name__ == "__main__":
    main()
