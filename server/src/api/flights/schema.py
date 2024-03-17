from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class FlightCreate(BaseModel):
    flight_number: str
    rocket_type: str
    launch_datetime: datetime
    launch_site: str
    payload: str
    orbit: str
    mission_objective: str
    launch_outcome: str
    booster_landing_success: bool
    anomalies: Optional[str] = None


class FlightPlanCreate(BaseModel):
    flight_id: int
    launch_window_start: datetime
    launch_window_end: datetime
    payload_mass: float
    destination_orbit: str
    mission_duration: int
    backup_date: datetime
    mission_objectives: str


class FlightPlanEventCreate(BaseModel):
    plan_id: int
    event_name: str
    planned_event_time: datetime
    target_altitude: float
    target_velocity: float
    target_latitude: float
    target_longitude: float
    target_orbit: str
