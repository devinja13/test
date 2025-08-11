import pandas as pd
import numpy as np
from typing import List, Tuple
import re




class ModelInputParserService:
    """
    This class is a Service which is primarly used to 
    parse the input from a dataframe into a gurobi linear 
    integer programming model format.
    """

    @staticmethod
    def get_names(df: pd.DataFrame) -> List[Tuple[str, str]]:
        """
        Returns a list of first name, last name tuples
        """
        names: List[str] = df['First Name Last Name'].tolist()
        separated_names: List[Tuple[str, str]] = [(name.split()[0], name.split()[1]) for name in names]
        return separated_names

    @staticmethod
    def get_emails(df: pd.DataFrame) -> List[str]:
        """
        Returns a list of email strings
        """
        emails: List[str] = df['Email Address'].tolist()
        return emails
    
    @staticmethod 
    def get_role_statuses(df: pd.DataFrame) -> List[int]:
        """
        Returns a list of ints: 1 represents DC Member, 0 
        represents observer
        """
        roles: List[int] = (df["Are you an Observer or DC Member?"] == "DC Member").astype(int).tolist()
        return roles
    
    @staticmethod
    def get_oc_statuses(df: pd.DataFrame) -> List[int]:
        """
        Returns a list of ints: 1 represents off campus,
        0 represents on campus
        """
        oc_statuses: List[int] = (df["Are you Off Campus (needed for Duncan Room Scheduling) "] == "Yes").astype(int).tolist()
        return oc_statuses
    
    @staticmethod
    def _format_shift_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats column names to be interpretable to model.
        ex. changes "Thursday [Mar 7] (evening shift)"
        to "March 7"
        """
        month_map = {
            "Jan": "January",
            "Feb": "February",
            "Mar": "March",
            "Apr": "April",
            "May": "May",
            "Jun": "June",
            "Jul": "July",
            "Aug": "August",
            "Sep": "September",
            "Oct": "October",
            "Nov": "November",
            "Dec": "December"
        }
        def format_shift_column(col: str) -> str:
            match = re.search(r'\[(.*?)\]', col)
            if match:
                shift = match.group(1)
                shift = shift.strip()
                # Remove trailing parentheses information 
                shift = re.sub(r'\s*\(.*?\)\s*$', '', shift)
                
                # Replace abbreviated month names with full names
                for abbr, full in month_map.items():
                    shift = re.sub(r'\b' + re.escape(abbr) + r'\b', full, shift)
                return shift
            else:
                return col
        df.columns = [format_shift_column(col) for col in df.columns]
        return df
        
        
            
    @staticmethod 
    def parse_df_to_model_input(df: pd.DataFrame):  
        """
        Parses the dataframe into model inputs:
        Returns (names, emails, role_statuses, oc_statuses, availability, dates)
        """
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df = df.sort_values('Timestamp').drop_duplicates(subset=['Email Address'], keep='last')

        names: List[Tuple[str, str]] = ModelInputParserService.get_names(df)
        emails: List[str] = ModelInputParserService.get_emails(df)
        role_statuses: List[int] = ModelInputParserService.get_role_statuses(df)
        oc_statuses: List[int] = ModelInputParserService.get_oc_statuses(df)

        df: pd.DataFrame = ModelInputParserService._format_shift_columns(df)
        
        availability: np.ndarray = df.iloc[:, 5:].values
        availability = np.nan_to_num(availability, nan = 0).astype(int)
        
        dates: List[str] = df.columns[5:].tolist()

        return {"names":names, 
                "emails": emails,
                "role_statuses": role_statuses,
                "oc_statuses": oc_statuses, 
                "availability": availability,
                "dates":dates}
       

    
