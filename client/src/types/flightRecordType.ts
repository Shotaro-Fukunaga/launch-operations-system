export interface FlightRecord {
  time: string;
  launch_relative_time:number;
  heading: number;
  altitude: number;
  latitude: number;
  longitude: number;
  orbital_speed: number;
  apoapsis_altitude: number;
  periapsis_altitude: number;
  inclination: number;
  eccentricity: number;
}

export interface EventRecord {
  time: string;
  level: string;
  msg: string;
}

export interface FlightEventRecord {
  flight_records: FlightRecord[];
  event_records: EventRecord[];
}
