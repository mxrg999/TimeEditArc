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
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not valid (expired, revoked, etc.), reauthenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print("Refreshing token failed:", str(e))
                # If refresh fails, delete the token.pickle and re-authenticate
                if os.path.exists('token.pickle'):
                    os.remove('token.pickle')
                creds = None
        else:
            creds = authenticate_user(SCOPES)

    # Proceed if creds are available
    if creds:
        try:
            service = build('calendar', 'v3', credentials=creds)
            return service
        except Exception as e:
            print("Error building the service:", str(e))
            return None
    else:
        return None

def authenticate_user(SCOPES):
    try:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        print("Saving credentials...")
        return creds
    except FileNotFoundError:
        print("Error: credentials.json file not found.")
    except Exception as e:
        print("Error initializing authentication flow:", str(e))
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
