#import pickle
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from config import settings

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
        ]

def getGoogleCredentials():
    creds = None
    # TODO: reimplement tokens caching at some point
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    #if os.path.exists('token.pickle'):
    #    with open('token.pickle', 'rb') as token:
    #        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = service_account.Credentials.from_service_account_file(
                    settings.SERVICE_ACCOUNT_FILE_PATH,
                    scopes=SCOPES)

        # Save the credentials for the next run
        #with open('token.pickle', 'wb') as token:
        #    pickle.dump(creds, token)

    return creds
