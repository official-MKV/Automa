from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError

secret_root = '.\secrets'

## TODO:getting service using client_secret
def create_service(client_secret,service,version):
    SCOPES = [f'https://www.googleapis.com/auth/{service}']
    creds = None
    if os.path.exists(f'{secret_root}\{service}_token.json'):
        creds = Credentials.from_authorized_user_file(f'{secret_root}\{service}_token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'{secret_root}\{service}_token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        serviceObj = build(service, version, credentials=creds)
        return serviceObj
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')




# TODO:getting service using service_account

def create_service_from_account(service_account_json):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(secret_root,service_account_json),
        scopes="https://www.googleapis.com/auth/drive",
    )
    service = build('drive', 'v3', credentials=credentials)
    return service