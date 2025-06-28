import json
import os
from decouple import config
from google.oauth2 import service_account
from pyfcm import FCMNotification


def get_fcm_object():
    credentials_path = config('GOOGLE_APPLICATION_CREDENTIALS')

    # Check if file exists
    if not os.path.exists(credentials_path):
        print('I should never be here')

    # Read the JSON file and convert to a dictionary
    with open(credentials_path) as f:
        gcp_json_credentials_dict = json.load(f)

    # Load credentials from JSON dictionary
    credentials = service_account.Credentials.from_service_account_info(
        gcp_json_credentials_dict, scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )

    fcm = FCMNotification(
        service_account_file=None, 
        credentials=credentials, 
        project_id=config('FIREBASE_PROJECT_ID')
    )

    return fcm
