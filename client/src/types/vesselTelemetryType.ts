export interface AtmosphereInfo {
  angle_of_attack: number;
  sideslip_angle: number;
  mach: number;
  dynamic_pressure: number;
  atmosphere_density: number;
  atmospheric_pressure: number;
  atmospheric_drag: number;
  terminal_velocity: number;
}

export interface OrbitInfo {
  orbital_speed: number;
  apoapsis_altitude: number;
  periapsis_altitude: number;
  period: number;
  time_to_apoapsis: number;
  time_to_periapsis: number;
  semi_major_axis: number;
  inclination: number;
  eccentricity: number;
  longitude_of_ascending_node: number;
  argument_of_periapsis: number;
  prograde: [number, number, number];
}


export interface SurfaceInfo {
  altitude_als: number;
  altitude_true: number;
  pitch: number;
  heading: number;
  roll: number;
  surface_speed: number;
  vertical_speed: number;
  surface_horizontal_speed: number;
  latitude: number;
  longitude: number;
  biome: string;
  situation: string;
}


export interface DeltaVItem {
  start_mass: number;
  end_mass: number;
  burned_mass: number;
  max_thrust: number;
  twr: number;
  slt: number;
  isp: number;
  atom_delta_v: number;
  vac_delta_v: number;
  time: number;
}

export interface DeltaVStatus {
  stage_delta_v_atom: number;
  stage_delta_v_vac: number;
  total_delta_v_atom: number;
  total_delta_v_vac: number;
  delta_v_list: DeltaVItem[];
}



export interface VesselTelemetryType {
  surface_info: SurfaceInfo;
  orbit_info: OrbitInfo;
  atmosphere_info: AtmosphereInfo;
  delta_v_status: DeltaVStatus;
}

