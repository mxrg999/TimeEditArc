# main.py
"""
    TimeEditArc - Your Personal Calendar Assistant
    ------------------------------------------------
    - Fetches iCalendar data from a specified URL.
    - Extracts and modifies event details, including course codes, names, and activity types.
    - Assigns distinct colors to events based on the course and activity type.
    - Supports dynamic color configurations, allowing users to exclude or prioritize certain colors.
    - Provides a user-friendly interface for managing multiple configuration profiles.
    - Uses the Google Calendar API to seamlessly create or update events on a target Google Calendar.
    - Offers an optional command-line argument to directly load and process a specific configuration.

    Created and maintained by @mxrg999
"""


import os
import argparse
from src.get_calendar_service import logout
from src.CalendarManager import CalendarManager
from src.ConfigManager import ConfigManager
from src.ICalManager import ICalManager

class TimeEditArcApp:

    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = None

    def run(self):
        self.load_config_from_args()
        if not self.config:
            self.main_menu()

    def load_config_from_args(self):
        parser = argparse.ArgumentParser(description="Manage and update Google Calendar events.")
        parser.add_argument('--config', type=str, help='Name of the configuration to load directly.')
        args = parser.parse_args()

        if args.config:
            self.config = self.config_manager.load_configuration_by_name(args.config)
            if self.config:
                print(f"Configuration '{args.config}' has been loaded successfully!\n")
                self.process_calendar()
            else:
                print(f"Error: Configuration '{args.config}' not found!")

    def main_menu(self):
        clear_screen()
        while True:
            choice = self.display_menu()
            self.handle_menu_choice(choice)

    def display_menu(self):
        config_name = self.config['config_name'] if self.config else '<No Config Selected>'
    
        menu_display = """
-------------------------------------
             TimeEditArc
-------------------------------------
Choose an option:
1. Set up a new configuration
2. Load an existing configuration
3. Remove a profile
4. Rename a profile
5. Log out from Google Calendar
6. Configure event colors
7. Process and update calendar using: {0}

Enter your choice (1/2/3/4/5/6/7): 
""".format(config_name)
    
        return input(menu_display)

    def handle_menu_choice(self, choice):
        if choice == '1':
            self.config = self.config_manager.setup_configuration()
        elif choice == '2':
            self.config = self.config_manager.load_configuration()
        elif choice == '3':
            self.config_manager.remove_profile()
        elif choice == '4':
            self.config_manager.rename_profile()
        elif choice == '5':
            clear_screen()
            logout()
        elif choice == '6':
            self.config = ensure_config_loaded(self.config_manager, self.config)
            if self.config:
                self.config_manager.configure_colors()
        elif choice == '7':
            clear_screen()
            self.config = ensure_config_loaded(self.config_manager, self.config)
            if self.config:
                proceed = input("Do you want to start the process of importing? (yes/no): ").lower()
                if proceed == 'yes' or proceed == 'y':
                    self.process_calendar()
                else:
                    clear_screen()
                    print("Process cancelled by the user.")

        else:
            clear_screen()
            print("Invalid choice. Please try again.")

    def process_calendar(self):
        ical_manager = ICalManager(self.config)
        ical_data = ical_manager.run()
        calendar_manager = CalendarManager(self.config)
        for event in ical_data.walk('vevent'):
            calendar_manager.create_or_update_event(event)
            calendar_manager.print_event(event)
        print("Your calendar has now been imported/updated.")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def ensure_config_loaded(config_manager, config):
    if not config:
        clear_screen()
        print("Configuration not loaded!")
        load_choice = input("Would you like to load an existing configuration? (yes/no): ").lower()
        if load_choice == 'yes' or load_choice == 'y':
            return config_manager.load_configuration()
        else:
            clear_screen()
            print("Please load or set up a configuration first.")
            return None
    return config


if __name__ == "__main__":
    app = TimeEditArcApp()
    app.run()
