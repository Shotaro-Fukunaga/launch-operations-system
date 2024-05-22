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
  event?: string;
  display_log?:string
}

export interface EventRecord {
  time: string;
  launch_relative_time:number;
  event: string;
  
}

export interface FlightEventRecord {
  flight_records: FlightRecord[];
  event_records: EventRecord[];
}
