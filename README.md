# iCalendar to Google Calendar Importer

A Python script to fetch events from an iCalendar URL and create/update them on a Google Calendar. 

## Table of Contents

- 🚀 [**Features**](#features)
- 📖 [**How to Use**](#how-to-use)
- 🔑 [**Google Calendar API Setup**](#obtaining-credentialsjson-for-google-calendar-api)

## Features:

- **iCalendar Integration**:
  - Fetches events from an iCalendar (`.ics`) URL.
  - Parses the iCalendar data to extract event details such as summary, start time, end time, location, description, and organizer.

- **Google Calendar Integration**:
  - Uses the Google Calendar API to authenticate and interact with your Google Calendar.
  - Creates events in a specified Google Calendar based on the events fetched from the iCalendar URL.
  - Supports customization of event colors with the default set to Tomato for this release.

- **Profile Management**:
  - Create, load, rename, and remove configuration profiles.
  - Keep multiple configurations and switch between them as needed.

## How to Use:

1. [Create and download credentials for Google Calendar API](#obtaining-credentialsjson-for-google-calendar-api)
2. Set up a virtual environment (`venv`) and install the necessary packages: 
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
3. Run the main.py script and follow the prompts to either set up a new configuration or load an existing one.
4. After selecting or creating a configuration, you can process and update your Google Calendar with the events from the iCalendar URL.

## Obtaining `credentials.json` for Google Calendar API:

1. **Google Cloud Console**:
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing project.

2. **Enable Google Calendar API**:
   - In the dashboard, click on "Navigation Menu" (three horizontal lines at the top left corner).
   - Navigate to `APIs & Services` > `Library`.
   - Search for "Google Calendar API" and select it.
   - Click the "Enable" button to activate the Google Calendar API for your project.

3. **Create Credentials**:
   - After enabling the API, click on "Create Credentials" and select "OAuth 2.0 Client IDs".
   - Choose the "Desktop app" application type.
   - Click "Create" to generate your credentials.

4. **Download `credentials.json`**:
   - Once the OAuth 2.0 Client ID is created, you'll see a screen listing your client IDs.
   - Find the client ID for the "Desktop app" type.
   - Click on the download icon (it looks like a downward arrow) on the right side of your client ID.
   - This will download the `credentials.json` file to your computer.

5. **Place in Project Directory**:
   - Move the downloaded `credentials.json` file to your project directory, where your `main.py` script resides.

Remember to never share your `credentials.json` file publicly, as it contains sensitive information related to your Google Cloud project.

---

Maintained by [@mxrg999](https://github.com/mxrg999)
