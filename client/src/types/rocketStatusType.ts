interface AntennaStatus {
  status: string;
  power: number;
  packet_interval: number;
  packet_size: number;
  packet_resource_cost: number;
}

interface SolarPanelStatus {
  status: string;
  energy_flow: number;
  sun_exposure: number;
}

interface ReactionWheelStatus {
  status: string;
  active: boolean;
  available_torque: [number, number, number]; // Tuple for pitch, yaw, roll
  max_torque: [number, number, number];
}

interface FairingStatus {
  status: string;
  dynamic_pressure: number;
  temperature: number;
  max_temperature: number;
}

export interface EngineStatus {
  status: string;
  start_mass: number;
  end_mass: number;
  burned_mass: number;
  max_thrust: number;
  twr: number;
  slt: number;
  isp: number;
  atom_delta_v: number;
  vac_delta_v: number;
  burn_time: number;
  temperature: number;
  max_temperature: number;
  // throttle: number;
}

interface ResourceStatus {
  name: string;
  amount: number;
  max: number;
}

export interface TankStatus {
  temperature: number;
  max_temperature: number;
  fuel?: ResourceStatus;
  lqd_oxygen?: ResourceStatus;
}

interface CommunicationStatus {
  can_communicate: boolean;
  can_transmit_science: boolean;
  signal_strength: number;
  signal_delay: number;
  total_comm_power: number;
  control_path: Array<{
    type: string;
    signal_strength: number;
  }>;
}

interface SatelliteBusStatus extends CommunicationStatus {
  status: string;
  shielded: boolean;
  current_charge: number;
  max_charge: number;
}

export interface RocketStatusType {
  antenna: AntennaStatus;
  fairing_1: FairingStatus;
  fairing_2: FairingStatus;
  main_tank: TankStatus;
  second_tank: TankStatus;
  main_engine: EngineStatus;
  second_engine: EngineStatus;
  solar_panel_1: SolarPanelStatus;
  solar_panel_2: SolarPanelStatus;
  reaction_wheel: ReactionWheelStatus;
  satellite_bus: SatelliteBusStatus;
}
