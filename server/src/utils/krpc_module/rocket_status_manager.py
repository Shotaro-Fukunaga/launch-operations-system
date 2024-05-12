from src.settings.config import GO, ACTIVE, CUTOFF
from src.utils.krpc_module.vessel_manager import VesselManager
from src.utils.krpc_module.part_unit import PartUnit
from src.utils.decorators.round_output import round_output
from src.utils.krpc_module.flight_dynamics import FlightDynamics
from krpc.services.spacecenter import Part

# from src.utils import clog

from src.utils.clog import Clog


clogger = Clog()


class RocketStatusManager:

    def __init__(self, vessel_manager: VesselManager):
        self.vessel_manager = vessel_manager
        self.units: list[PartUnit] = vessel_manager.units.values()
        self.flight_dynamics = FlightDynamics(self.vessel_manager.vessel)
        self.flight_info = self.vessel_manager.flight_info
        self.vessel = self.vessel_manager.vessel

    def active_check(self, unit: PartUnit, msg: str = None, custom_cond: bool = True) -> None:
        try:
            if unit.part and unit.status == GO and custom_cond:
                unit.status = ACTIVE
                msg = msg or f"{unit.unit_name.capitalize().replace('_', ' ')} ACTIVE"
                clogger.info(msg, True)
        except Exception as e:
            clogger.error(f"Error in active_check for unit {unit.unit_name}: {e}")

    def cutoff_check(self, unit: PartUnit, msg: str = None) -> None:
        try:
            if not unit.part and unit.status != CUTOFF:
                unit.status = CUTOFF
                msg = msg or f"{unit.unit_name.capitalize().replace('_', ' ')} Cutoff."
                clogger.info(msg, True)
        except Exception as e:
            clogger.error(f"Error in cutoff_check for unit {unit.unit_name}: {e}")

    @round_output
    def get_rocket_status(self):
        status_methods = {
            "antenna": self.get_antenna_status,
            "solar_panel_1": self.get_solar_panel_status,
            "solar_panel_2": self.get_solar_panel_status,
            "reaction_wheel": self.get_reaction_wheel_status,
            "satellite_bus": self.get_satellite_bus_status,
            "fairing_1": self.get_fairing_status,
            "fairing_2": self.get_fairing_status,
        }

        result = {name: method(name) for name, method in status_methods.items()}
        main_stage_status = self.get_main_stage_status()
        second_stage_status = self.get_second_stage_status()

        return {**result, **main_stage_status, **second_stage_status}

    @staticmethod
    def safe_getattr(obj, attr, default=0):
        return getattr(obj, attr, default) if obj else default

    @staticmethod
    def get_status_values(status, obj, keys_defaults: dict[str, any]):
        result = {"status": status}
        for key, default in keys_defaults.items():
            try:
                if status == CUTOFF:
                    result[key] = default
                else:
                    # 例外処理の追加
                    result[key] = getattr(obj, key, default)
            except AttributeError as e:
                clogger.error(f"AttributeError: {e} - Setting default value for key '{key}'")
                result[key] = default
            except Exception as e:
                clogger.error(f"Unexpected error: {e} - Setting default value for key '{key}'")
                result[key] = default
        return result

    def get_antenna_status(self, unit_name: str):
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        keys_defaults = {"power": 0, "packet_interval": 0, "packet_size": 0, "packet_resource_cost": 0}
        return self.get_status_values(status=unit.status, obj=unit.part.antenna, keys_defaults=keys_defaults)

    def get_solar_panel_status(self, unit_name: str):
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        if unit.part and hasattr(unit.part, "solar_panel"):
            self.active_check(unit=unit, custom_cond=unit.part.solar_panel.deployed)
        keys_defaults = {"energy_flow": 0, "sun_exposure": 0}
        return self.get_status_values(unit.status, unit.part.solar_panel, keys_defaults)

    def get_reaction_wheel_status(self, unit_name: str):
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        keys_defaults = {"active": False, "available_torque": (0.0, 0.0, 0.0), "max_torque": (0.0, 0.0, 0.0)}
        return self.get_status_values(unit.status, unit.part.reaction_wheel, keys_defaults)

    def get_communication_status(self):
        comm = self.vessel.comms
        return {
            "can_communicate": comm.can_communicate,
            "can_transmit_science": comm.can_transmit_science,
            "signal_strength": comm.signal_strength,
            "signal_delay": comm.signal_delay,
            "total_comm_power": comm.power,
        }

    def get_satellite_bus_status(self, unit_name: str):
        unit = self.vessel_manager.get_unit_by_name(unit_name)

        self.active_check(unit, "Satellite Bus Active", not unit.part.shielded)
        bus_status = {
            "status": unit.status,
            "shielded": unit.part.shielded,
            "current_charge": unit.part.resources.amount("ElectricCharge"),
            "max_charge": unit.part.resources.max("ElectricCharge"),
        }
        communication_status = self.get_communication_status()
        return {**bus_status, **communication_status}

    def get_fairing_status(self, unit_name: str):
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        self.cutoff_check(unit=unit, msg="Fairing Jettisoned.")
        keys_defaults = {"dynamic_pressure": 0, "temperature": 0, "max_temperature": 0}
        return self.get_status_values(unit.status, unit.part, keys_defaults)

    def get_tank_status(self, part: Part | None, status: int) -> dict[dict]:
        resource_dict = {
            "status": status,
            "temperature": 0,
            "max_temperature": 0,
            "lqd_oxygen": {"name": "", "amount": 0, "max": 0},
            "fuel": {"name": "", "amount": 0, "max": 0},
        }

        try:
            if part:
                resource_dict["temperature"] = getattr(part, "temperature", 0)
                resource_dict["max_temperature"] = getattr(part, "max_temperature", 0)

                if hasattr(part, "resources") and part.resources:
                    for resource in part.resources.all:
                        dict_key = "lqd_oxygen" if resource.name == "LqdOxygen" else "fuel"
                        resource_dict[dict_key] = {
                            "name": resource.name,
                            "amount": resource.amount,
                            "max": resource.max,
                        }
        except AttributeError as e:
            clogger.error(f"AttributeError in get_tank_status for part {part}: {e}")
        except Exception as e:
            clogger.error(f"Unexpected error in get_tank_status: {e}")

        return resource_dict

    def get_main_stage_status(self):
        main_engine = self.vessel_manager.get_unit_by_name("main_engine")
        main_tank = self.vessel_manager.get_unit_by_name("main_tank")

        if main_engine.part and hasattr(main_engine.part, "engine"):
            is_active = main_engine.part.engine.active
            self.active_check(main_engine, f"{main_engine.unit_name.capitalize().replace('_', ' ')} Ignition", is_active)
            self.active_check(unit=main_tank, custom_cond=is_active)

        self.cutoff_check(main_engine, "MECO main engine cutoff.")
        self.cutoff_check(main_tank)

        start_mass = self.vessel.mass
        main_engine_status = self.calculate_engine_metrics(main_engine.part, main_engine.status, start_mass)
        main_tank_status = self.get_tank_status(main_tank.part, main_tank.status)

        return {
            "main_engine": main_engine_status,
            "main_tank": main_tank_status,
        }

    def get_second_stage_status(self):
        second_engine = self.vessel_manager.get_unit_by_name("second_engine")
        second_tank = self.vessel_manager.get_unit_by_name("second_tank")

        if second_engine.part and hasattr(second_engine.part, "engine"):
            is_active = second_engine.part.engine.active
            self.active_check(second_engine, f"{second_engine.unit_name.capitalize().replace('_', ' ')} Ignition", is_active)
            self.active_check(unit=second_tank, custom_cond=is_active)
        self.cutoff_check(second_engine, "SECO second engine cutoff.")
        self.cutoff_check(second_tank)

        start_mass = self.vessel.mass

        second_engine_status = self.calculate_engine_metrics(second_engine.part, second_engine.status, start_mass)
        second_tank = self.get_tank_status(second_tank.part, second_tank.status)

        return {
            "second_engine": second_engine_status,
            "second_tank": second_tank,
        }

    def calculate_engine_metrics(self, part: Part | None, status: int, start_mass: float) -> dict:
        if part and hasattr(part, "engine"):
            engine = part.engine
            thrust = engine.thrust
            max_thrust = engine.max_thrust
            temperature = part.temperature
            max_temperature = part.max_temperature
            available_thrust = engine.available_thrust
            vac_isp = engine.vacuum_specific_impulse
            current_pressure_atm = self.flight_info.static_pressure / 101325
            atom_isp = engine.specific_impulse_at(pressure=current_pressure_atm)
            fuel_mass = sum(propellant.total_resource_available for propellant in engine.propellants)
        else:
            thrust = 0
            max_thrust = 0
            temperature = 0
            max_temperature = 0
            available_thrust = 0
            vac_isp = 0
            atom_isp = 0
            fuel_mass = 0

        vac_delta_v = self.flight_dynamics.calculate_delta_v(vac_isp, fuel_mass, start_mass)
        atom_delta_v = self.flight_dynamics.calculate_delta_v(atom_isp, fuel_mass, start_mass)
        burn_time = self.flight_dynamics.burn_time_estimation(atom_isp, fuel_mass, max_thrust)
        end_mass = start_mass - fuel_mass
        twr = thrust / (start_mass * 9.81) if start_mass > 0 else 0
        slt = available_thrust / (start_mass * 9.81) if start_mass > 0 else 0

        return {
            "status": status,
            "start_mass": start_mass if part else 0,
            "end_mass": end_mass if part else 0,
            "burned_mass": fuel_mass,
            "max_thrust": max_thrust,
            "twr": twr,
            "slt": slt,
            "isp": atom_isp,
            "atom_delta_v": atom_delta_v,
            "vac_delta_v": vac_delta_v,
            "burn_time": burn_time,
            "temperature": temperature,
            "max_temperature": max_temperature,
        }
