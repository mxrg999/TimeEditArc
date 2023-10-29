# main.py
"""
    Fetches iCalendar data from a URL, modifies the data, and creates or updates events on a Google Calendar.
    The modified data includes extracted course codes and names, activity types, and assigned colors based on course and activity.
    The script uses the Google Calendar API to create or update events on a target Google Calendar.

    Created and maintained by @mxrg999
"""

from src.get_calendar_service import logout
from src.CalendarManager import CalendarManager
from src.ConfigManager import ConfigManager
from src.ICalManager import ICalManager
import os

def main():
    config_manager = ConfigManager()
    config = None
    clear_screen()
    while True:

        try:
            config_name = config['config_name']
        except:
            config_name = '<No Config Selected>'

        choice = input(f"Choose an option: \
                       \n1. Set up a new configuration \
                       \n2. Load an existing configuration \
                       \n3. Remove a profile \
                       \n4. Rename a profile \
                       \n5. Log out from Google Calendar\
                       \n6. Configure event colors \
                       \n7. Process and update calendar using: {config_name}\
                       \nEnter your choice (1/2/3/4/5/6/7): ")
        if choice in ['1', '2']:
            if choice == '1':
                clear_screen()
                config = config_manager.setup_configuration()
            elif choice == '2':
                clear_screen()
                config = config_manager.load_configuration()
            ical_manager = ICalManager(config)
            calendar_manager = CalendarManager(config)
        elif choice == '3':
            clear_screen()
            config_manager.remove_profile()
            continue
        elif choice == '4':
            clear_screen()
            config_manager.rename_profile()
            continue
        elif choice == '5':
            clear_screen()
            logout()
            continue
        elif choice == '6':
            config = ensure_config_loaded(config_manager, config)
            if config:
                config_manager.configure_colors()
        elif choice == '7':
            clear_screen()
            config = ensure_config_loaded(config_manager, config)
            if config:
                ical_manager = ICalManager(config)
                ical_data = ical_manager.run()
            
                calendar_manager = CalendarManager(config)
                for event in ical_data.walk('vevent'):
                    calendar_manager.create_or_update_event(event)
                    calendar_manager.print_event(event)
                print("Your calendar has now been imported/updated.")
                break
        else:
            clear_screen()
            print("Invalid choice. Please try again.")
            continue

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_config_loaded(config_manager, config):
    if not config:
        print("Configuration not loaded!")
        load_choice = input("Would you like to load an existing configuration? (yes/no): ").lower()
        if load_choice == 'yes':
            config = config_manager.load_configuration()
            if not config:
                return None
        else:
            print("Please load or set up a configuration first.")
            return None
    return config

if __name__ == "__main__":
    main()
