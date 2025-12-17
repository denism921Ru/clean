import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_service():
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if not creds_json:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS_JSON is not set")

    creds = Credentials.from_service_account_info(
        eval(creds_json),
        scopes=SCOPES
    )

    return build("sheets", "v4", credentials=creds)


def append_row(sheet_name: str, values: list):
    service = get_service()
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_name,
        valueInputOption="USER_ENTERED",
        body={"values": [values]},
    ).execute()
