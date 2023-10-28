# ConfigManager.py

import configparser

class ConfigManager:
    def __init__(self, config=None):
        self.config = config if config else {}
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('config.ini')

    def load_configuration(self):
        config_name = input("Which configuration would you like to use? Available: " + ", ".join(self.config_parser.sections()) + "\n")

        if config_name not in self.config_parser:
            print(f"Error: Configuration '{config_name}' not found!")
            exit(1)

        self.config = self.config_parser[config_name]
        return self.config

    def setup_configuration(self):
        """Prompt the user for configuration values and save them."""
        config_name = input("Enter configuration name (e.g., development, production): \n")

        calendar_id = input(f"Enter calendar ID for {config_name}: ")
        ical_url = input(f"Enter iCal URL for {config_name}: ")

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')  # Read existing configurations

        self.config[config_name] = {
            'calendar_id': calendar_id,
            'ical_url': ical_url,
            'time_zone': 'Etc/GMT'
        }

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        
        print(f"Configuration '{config_name}' has been saved and loaded successfully! ")
        return self.config[config_name] 


    def remove_profile(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Display available profiles
        print("Available profiles:")
        for section in self.config.sections():
            print(section)

        # Prompt for the profile to remove
        profile_to_remove = input("Enter the name of the profile you wish to remove: ")

        # Check if the profile exists
        if profile_to_remove in self.config:
            # Remove the profile
            self.config.remove_section(profile_to_remove)

            # Save changes
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            print(f"Profile '{profile_to_remove}' has been removed successfully!")
        else:
            print(f"Profile '{profile_to_remove}' does not exist!")


    def rename_profile(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Display available profiles
        print("Available profiles:")
        for section in self.config.sections():
            print(section)

        # Prompt for the profile to rename
        profile_to_rename = input("Enter the name of the profile you wish to rename: ")

        # Check if the profile exists
        if profile_to_rename in self.config:
            # Ask for the new name
            new_name = input("Enter the new name for the profile: ")

            # Check if the new name already exists
            if new_name in self.config:
                print(f"Profile '{new_name}' already exists! Choose a different name.")
                return

            # Rename the profile
            self.config[new_name] = self.config[profile_to_rename]
            self.config.remove_section(profile_to_rename)

            # Save changes
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            print(f"Profile '{profile_to_rename}' has been renamed to '{new_name}' successfully!")
        else:
            print(f"Profile '{profile_to_rename}' does not exist!")
