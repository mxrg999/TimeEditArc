# ConfigManager.py

import configparser
import os

class ConfigManager:
    def __init__(self, config=None):
        self.config = config if config else {}
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('config/config.ini')

    def setup_configuration(self):
        """Prompt the user for configuration values and save them."""
        clear_screen()
        config_name = input("Enter configuration name (e.g., development, production): \n")
        calendar_id = input(f"Enter calendar ID for {config_name}: ")
        ical_url = input(f"Enter iCal URL for {config_name}: ")

        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')

        self.config[config_name] = {
            'config_name': config_name,
            'calendar_id': calendar_id,
            'ical_url': ical_url,
            'time_zone': 'Etc/GMT',
            'excluded_colors': '',	
        }

        with open('config/config.ini', 'w') as configfile:
            self.config.write(configfile)

        clear_screen()
        print(f"Configuration '{config_name}' has been saved and loaded successfully!")
        return self.config[config_name]

    def load_configuration(self):
        """Load an existing configuration."""
        clear_screen()
        self.config_parser.read('config/config.ini') 
        available_configs = self.config_parser.sections()
    
        while True:  # Loop until a valid config name is provided or user decides to exit
            # Display available configurations
            print("Available configurations:")
            for config in available_configs:
                print(f"- {config}")
            print("")
    
            config_name = input("Which configuration would you like to use? \nOr type 'exit' to cancel.\n")
    
            if config_name in available_configs:
                self.config = self.config_parser[config_name]
                clear_screen()
                print(f"Configuration '{config_name}' has been loaded successfully!")
                return self.config
    
            elif config_name.lower() == 'exit':
                clear_screen()
                print("Configuration loading cancelled.")
                return None
    
            else:
                clear_screen()
                print(f"Error: Configuration '{config_name}' not found! Please try again or type 'exit' to cancel.\n")


    def load_configuration_by_name(self, config_name):
        """Load a configuration by its name directly."""
        self.config_parser.read('config/config.ini')

        if config_name in self.config_parser:
            self.config = self.config_parser[config_name]
            return self.config
        else:
            return None

    def remove_profile(self):
        clear_screen()
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')

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
            with open('config/config.ini', 'w') as configfile:
                self.config.write(configfile)
            clear_screen()
            print(f"Profile '{profile_to_remove}' has been removed successfully!")
        else:
            clear_screen()
            print(f"Profile '{profile_to_remove}' does not exist!")

    def rename_profile(self):
        clear_screen()
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')

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
                print(f"Profile '{new_name}' already exists! Choose a different name.\n")
                return

            # Rename the profile
            self.config[new_name] = self.config[profile_to_rename]
            self.config.remove_section(profile_to_rename)

            # Save changes
            with open('config/config.ini', 'w') as configfile:
                self.config.write(configfile)
            clear_screen()
            print(f"Profile '{profile_to_rename}' has been renamed to '{new_name}' successfully!")
        else:
            clear_screen()
            print(f"Profile '{profile_to_rename}' does not exist!")

    def configure_colors(self):
        colors = {
            "1": "Lavender", 
            "2": "Sage", 
            "3": "Grape", 
            "4": "Flamingo", 
            "5": "Banana", 
            "6": "Tangerine", 
            "7": "Peacock", 
            "8": "Graphite", 
            "9": "Blueberry", 
            "10": "Basil", 
            "11": "Tomato"
        }
    
        # First, ensure that the correct section exists in the config
        if not self.config:
            print("No configuration is currently loaded. Please load a configuration first.")
            return
    
        if self.config['config_name'] not in self.config_parser:
            print(f"Error: Configuration '{self.config['config_name']}' not found!")
            return
        
        config_name = self.config['config_name']

       # Load current excluded colors
        if self.config_parser.has_option(config_name, 'excluded_colors'):
            excluded_colors_str = self.config_parser.get(config_name, 'excluded_colors')
        else:
            excluded_colors_str = ''

        excluded_colors = excluded_colors_str.split(',') if excluded_colors_str else []

        while True:
            # Display available colors
            clear_screen()
            print("Available colors:")
            for key, value in colors.items():
                if key in excluded_colors:
                    print(f"{key}. {value} (Excluded)")
                else:
                    print(f"{key}. {value}")
    
            # Toggle colors
            choice = input("Enter the number of the color to toggle or 'done' to finish: ")
    
            if choice in colors.keys():
                if choice in excluded_colors:
                    excluded_colors.remove(choice)
                else:
                    excluded_colors.append(choice)
            elif choice == 'done':
                break
            else:
                print("Invalid choice. Please enter a valid number or 'done' to finish.")
    
         # Update the excluded_colors in the configuration
        self.config_parser.set(config_name, 'excluded_colors', ",".join(excluded_colors))

        # Save the updated configuration to the file
        with open('config/config.ini', 'w') as configfile:
            self.config_parser.write(configfile)

        clear_screen()
        print("Colors have been configured successfully!")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')