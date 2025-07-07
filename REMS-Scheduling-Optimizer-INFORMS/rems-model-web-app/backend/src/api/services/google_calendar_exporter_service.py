
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from datetime import datetime
import re
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarExporterService:
    """
    This class is a Service which is primarily used for exporting the potentially
    client-side modified gurobi optimized schedule to the authenticated user's 
    person google calendar.
    """

    @staticmethod
    def _month_to_number(month_name):
        """Convert month name to its numerical representation"""
        months = {
            "January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"
        }
        return months.get(month_name, "01")

    @staticmethod
    def _format_schedule(schedule: list):
        current_year = datetime.now().year
        formatted_schedule = []
        for assignment in schedule:
            new_schedule_item = {}
            new_schedule_item["name"] = f"{assignment['first_name']} {assignment['last_name']}"
            new_schedule_item["email"] = assignment["email"]

            # Parse the shift date string (e.g., "Mon, March 31, 8AM")
            shift_str = assignment.get('shift', '')
            
            # Extract components using regex
            pattern = r"([A-Za-z]+),\s+([A-Za-z]+)\s+(\d+),\s+(\d+)([AP]M)"
            match = re.match(pattern, shift_str)
            
            if match:
                weekday, month, day, hour, am_pm = match.groups()
                
                # Convert day to int for formatting
                day_int = int(day)
                
                # Convert hour to 24-hour format
                hour = int(hour)
                if am_pm.upper() == 'PM' and hour < 12:
                    hour += 12
                elif am_pm.upper() == 'AM' and hour == 12:
                    hour = 0
                    
                # Create datetime dictionary
                new_schedule_item["datetime"] = {
                    "weekday": weekday,
                    "month": month,
                    "day": day_int,
                    "hour": hour,
                    "am_pm": am_pm,
                    "year": current_year,
                    # Create formatted strings for Google Calendar
                    "iso_start": f"{current_year}-{GoogleCalendarExporterService._month_to_number(month)}-{day_int:02d}T{hour:02d}:00:00",
                    "iso_end": f"{current_year}-{GoogleCalendarExporterService._month_to_number(month)}-{day_int:02d}T{hour+1:02d}:00:00"
                }
            else:
                # Fallback if parsing fails
                new_schedule_item["datetime"] = {
                    "original": shift_str,
                    "year": current_year
                }
                
            formatted_schedule.append(new_schedule_item)
        
        return formatted_schedule

    @staticmethod
    def create_google_calendar(authAccessToken: str, schedule: list):

        # Construct the credentials object needed to access the user's google calendar
        credentials_obj = Credentials(
            token=authAccessToken,
            token_uri=os.getenv("GOOGLE_TOKEN_URI"),
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
        )

        formatted_schedule = GoogleCalendarExporterService._format_schedule(schedule)

        try:
            service = build("calendar", "v3", credentials = credentials_obj)
            for assignment in formatted_schedule:
                event = {
                "summary": f"REMS Shift: {assignment['name']}",
                "description": f"Scheduled REMS shift for {assignment['name']}",
                "location": "Rice University",
                "colorId": 6,
                "start": {
                    "dateTime": assignment["datetime"]["iso_start"],
                    "timeZone": "America/Chicago",
                },
                "end": {
                    "dateTime": assignment["datetime"]["iso_end"],
                    "timeZone": "America/Chicago"
                },
                "attendees": [
                    # {"email": assignment["email"]},
                ]
                 }

                event = service.events().insert(calendarId = "primary", body = event).execute()
            
        except HttpError as error:
            print(error)
            