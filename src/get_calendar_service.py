# get_calendar_service.py

import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def get_calendar_service():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Check if token.pickle file exists
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print("Error loading token.pickle:", str(e))
            return None

    # If no credentials available, prompt user to log in
    if not creds or not creds.valid:
        print("Fetching credentials...")
        print("Please log in to your Google account to continue.")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                print("Error: credentials.json file not found.")
                return None
            except Exception as e:
                print("Error initializing authentication flow:", str(e))
                return None

        # Save the credentials for the next run
        try:
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            print("Saving credentials...")
        except Exception as e:
            print("Error saving token.pickle:", str(e))
            return None

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print("Error building the service:", str(e))
        return None

def logout():
    if os.path.exists('token.pickle'):
        try:
            os.remove('token.pickle')
            print("Logged out successfully!")
        except Exception as e:
            print("Error logging out:", str(e))
    else:
        print("Already logged out.")
