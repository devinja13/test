from fastapi import APIRouter, HTTPException, Request
from typing import Any
from ..services.google_sheets_service import GoogleSheetsService
from ..services.model_input_parser_service import ModelInputParserService
from ..services.gurobi_scheduler_optimizer_service import GurobiSchedulerOptimizerService
from ..services.google_calendar_exporter_service import GoogleCalendarExporterService
from pydantic import BaseModel
from typing import Dict, Optional, List
import json
import pandas as pd


"""

"""
class SpreadsheetData(BaseModel):
    fileId: str

class CalendarExportRequest(BaseModel):
    schedule: List[Dict[str, Any]]
    calendar_id: Optional[str] = "primary"



router = APIRouter(
    prefix= "/schedules",
    tags = ["Schedules"]
)

@router.post("/")
async def create_schedule(request:Request, data: SpreadsheetData):

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    auth_access_token = auth_header.split(" ")[1]
    # Step One: Parsing the google sheet into a dataframe
    df: pd.DataFrame = GoogleSheetsService.create_scheduler_input_df(data.fileId, auth_access_token)
    # Step Two: Translating the dataframe into gurobi optimization model input
    print(df.columns)
    model_inputs: Dict[str, any] = ModelInputParserService.parse_df_to_model_input(df)

    names = model_inputs["names"]
    emails = model_inputs["emails"]
    role_statuses = model_inputs["role_statuses"]
    oc_statuses = model_inputs["oc_statuses"]
    availability = model_inputs["availability"]
    dates = model_inputs["dates"]
    
    # Step Three: Calling Schedule Optimizer service and getting raw outputs for scheduling
    gurobi_schedule_optimizer_service = GurobiSchedulerOptimizerService(**model_inputs)
    schedule: List[Dict[str, str]] = gurobi_schedule_optimizer_service.generate_optimized_schedule()
    # Step Four: Coercing some of the model outputs (oc_statuses, roles, availability) to Strings

    print(schedule)
    

    return {
        "success": True,
        "schedule": schedule
    }

@router.post("/{schedule_id}/export-calendar")
async def export_calendar(schedule_id: str, request: Request, data: CalendarExportRequest):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    auth_access_token = auth_header.split(" ")[1]
    schedule = data.schedule
    GoogleCalendarExporterService.create_google_calendar(authAccessToken = auth_access_token, schedule= schedule)

    print(f"Exported schedule for schedule_id: {schedule_id}")