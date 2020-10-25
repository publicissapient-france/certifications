from __future__ import print_function
import csv
import requests
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.pickle.
SCOPES = [
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
        ]
SERVICE_ACCOUNT_FILE = 'FIXME'
SPREADSHEET_ID = 'FIXME'



def getGoogleCredentials():
    creds = None
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
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def main():

    #service = build('drive', 'v3', credentials=creds)

    ## Call the Drive v3 API
    #results = service.files().list(
    #    pageSize=10, fields="nextPageToken, files(id, name)").execute()
    #items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

    print("1")
    service = build('sheets', 'v4', credentials=creds)
    print("2")
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='Kubernetes').execute()
    print("3")
    output_file = f'bla.csv'

    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(result.get('values'))

    f.close()

if __name__ == '__main__':
    main()
