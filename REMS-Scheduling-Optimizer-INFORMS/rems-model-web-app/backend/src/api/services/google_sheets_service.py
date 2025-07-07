import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import gspread



class GoogleSheetsService:
    """
    This class is a Service which is primarily used for creating a pandas df
    by accessing the spreadsheet uploaded by the user using the file id and 
    authentication token.
    """

    @staticmethod
    def create_scheduler_input_df(fileId: str, authAccessToken: str):
        
        # Construct the credentials object needed to access the google sheet
        credentials_obj = Credentials(
            token=authAccessToken,
            token_uri=os.getenv("GOOGLE_TOKEN_URI"),
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
        )

        # parsing the spreadsheet
        try: 
            service = build("sheets", "v4", credentials = credentials_obj)

            #calling sheets api
            # Get spreadsheet metadata first to find sheet names
            sheet_service = service.spreadsheets()
            spreadsheet = sheet_service.get(spreadsheetId = fileId).execute()
            first_sheet_name = spreadsheet['sheets'][0]['properties']['title']

            #gspread client
            gc = gspread.authorize(credentials_obj)
            
            # open the spreadsheet
            gc_spreadsheet = gc.open_by_key(fileId)
            gc_worksheet = gc_spreadsheet.worksheet(first_sheet_name)

            df = get_as_dataframe(gc_worksheet)

        except HttpError as error:
            print(error)
        return df
