export interface FlightRecord {
  time: string;
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
  x: string;
  time: string;
  event_type: string;
  event_details: string;
  event_level: number;
}

export interface FlightEventRecord {
  flight_records: FlightRecord[];
  event_records: EventRecord[];
}
