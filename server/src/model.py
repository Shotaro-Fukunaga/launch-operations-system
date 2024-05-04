from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field, validator
from typing import Optional


class LaunchParameters(BaseModel):
    launch_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(seconds=30))
    target_periapsis: Optional[int] = Field(200000, ge=0, description="Target periapsis in kilometers")
    target_apoapsis: Optional[int] = Field(200000, ge=0, description="Target apoapsis in kilometers")
    target_orbit_inc: Optional[float] = Field(39.39, ge=0, le=180, description="Target orbital inclination in degrees")

    @validator("target_periapsis", "target_apoapsis", pre=True, always=True)
    def check_positive(cls, value):
        if value is not None:
            assert value >= 0, "Value must be non-negative"
        return value

    @validator("target_orbit_inc", pre=True, always=True)
    def check_inclination_range(cls, value):
        if value is not None:
            assert 0 <= value <= 180, "Inclination must be between 0 and 180 degrees"
        return value


from typing import Optional

class TargetOrbit(BaseModel):
    periapsis: int
    apoapsis: int
    inclination: float
    speed: int

class LaunchCommand(BaseModel):
    launch_date: datetime
    command: str
    target_orbit: Optional[TargetOrbit]