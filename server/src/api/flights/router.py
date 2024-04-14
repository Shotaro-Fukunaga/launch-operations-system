import json
import logging


import krpc
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from src.models.model import FlightPlanEvents, FlightPlans, Flights
from src.settings.database import get_db
from src.utils.krpc_module.rocket_telemetry import RocketTelemetry
from .schema import FlightCreate, FlightPlanCreate, FlightPlanEventCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/{version}/flight",
    tags=["Flight"],
)

rocket = RocketTelemetry()

@router.get("/aaa")
def get_satellite_bus_status():
    return rocket.get_satellite_bus_status()

@router.post("", response_model=FlightCreate)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    db_flight = Flights(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


@router.post("/plans", response_model=FlightPlanCreate)
def create_flight_plan(flight_plan: FlightPlanCreate, db: Session = Depends(get_db)):
    db_flight_plan = FlightPlans(**flight_plan.dict())
    db.add(db_flight_plan)
    db.commit()
    db.refresh(db_flight_plan)
    return db_flight_plan


@router.post("/plan_events", response_model=FlightPlanEventCreate)
def create_flight_plan_event(flight_plan_event: FlightPlanEventCreate, db: Session = Depends(get_db)):
    db_flight_plan_event = FlightPlanEvents(**flight_plan_event.dict())
    db.add(db_flight_plan_event)
    db.commit()
    db.refresh(db_flight_plan_event)
    return db_flight_plan_event


# ロケットのステータスを返却するエンドポイント
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     conn = krpc.connect(name="sample")
#     vessel = conn.space_center.active_vessel
#     reference_frame = vessel.orbit.body.reference_frame
#     while True:
#         # 船舶の測定データを取得
#         vessel_data = get_measured_vessel_data(vessel, reference_frame)
#         # 重要な軌道データを取得
#         orbit_data = get_important_orbit_data(vessel, reference_frame)

#         # 二つの辞書を統合
#         vessel_data.update(orbit_data)

#         await websocket.send_text(json.dumps(vessel_data))

    
@router.get("/get_telemetory")
def get_telemetory():
    return {"telemetory": "test"}




# ロケットのスケジュールを登録するエンドポイント

# ロケットのスケジュールを返却するエンドポイント

# ロケットのログを取得するエンドポイントwebsocket
