import os.path
import requests  # Import the requests module
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

reading = "/Users/lerosevan/Downloads/Python/email_reader.py"

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_credentials():
    creds = None
    # Check if token.json exists and contains valid credentials.
    if os.path.exists("token.json"):
        #creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        os.remove("token.json")

    # If credentials are available and valid, forcibly log out the user.
    if creds and creds.valid:
        revoke_google_token(creds.token)  # Use the actual token for revocation.
        creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the author0ization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds
    
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

def revoke_google_token(token):
    response = requests.post('https://oauth2.googleapis.com/revoke',
                             params={'token': token},
                             headers={'content-type': 'application/x-www-form-urlencoded'})
    if response.status_code == 200:
        print("Token successfully revoked")
    else:
        print("Failed to revoke token")

if __name__ == "__main__":
    main()