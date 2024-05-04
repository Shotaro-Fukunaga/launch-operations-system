// import React, { createContext, useState, useEffect, ReactNode } from "react";
// import { VesselTelemetryType } from "../types/vesselTelemetryType";
// import { RocketStatusType } from "../types/rocketStatusType";
// import { FlightEventRecord } from "../types/flightRecordType";

// export type WebSocketContextType = {
//   sendMessage: (endpoint: string, message: string) => void;
//   messages: {
//     vesselTm: VesselTelemetryType | undefined;
//     rocketStatus: RocketStatusType | undefined;
//     flightEventRecord: FlightEventRecord | undefined;
//   };
// };

// type WebSocketProviderProps = {
//   children: ReactNode;
// };

// export const WebSocketContext = createContext<WebSocketContextType | null>(
//   null
// );

// export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
//   children,
// }) => {
//   const [vesselTmData, setVesselTmData] = useState<VesselTelemetryType>();
//   const [vesselTmWS, setVesselTmWS] = useState<WebSocket | null>(null);
//   const [rocketStatusData, setRocketStatusData] = useState<RocketStatusType>();
//   const [rocketStatusWS, setRocketStatusWS] = useState<WebSocket | null>(null);
//   const [flightEventRecordData, setFlightEventRecordData] =
//     useState<FlightEventRecord>();
//   const [flightEventRecordWS, setFlightEventRecordWS] =
//     useState<WebSocket | null>(null);

//   useEffect(() => {
//     const endpoints = [
//       {
//         url: "ws://localhost:8000/ws/vessel-telemetry",
//         setWs: setVesselTmWS,
//         setMessage: setVesselTmData,
//       },
//       {
//         url: "ws://localhost:8000/ws/rocket-status",
//         setWs: setRocketStatusWS,
//         setMessage: setRocketStatusData,
//       },
//       {
//         url: "ws://localhost:8000/ws/flight-records",
//         setWs: setFlightEventRecordWS,
//         setMessage: setFlightEventRecordData,
//       },
//     ];

//     endpoints.forEach(({ url, setWs, setMessage }) => {
//       const websocket = new WebSocket(url);
//       websocket.onopen = () => {
//         console.log(`Connected to ${url}`);
//         setWs(websocket);
//       };
//       websocket.onmessage = (evt) => {
//         try {
//           const data = JSON.parse(evt.data);
//           setMessage(data);
//         } catch (error) {
//           console.error("Error parsing JSON!", error);
//         }
//       };
//       websocket.onclose = () => {
//         console.log(`Disconnected from ${url}`);
//         setWs(null);
//       };
//     });

//     return () => {
//       endpoints.forEach(({ setWs }) => {
//         setWs((ws) => {
//           if (ws) ws.close();
//           return null;
//         });
//       });
//     };
//   }, []);

//   const sendMessage = (endpoint: string, message: string) => {
//     const websockets: { [key: string]: WebSocket | null } = {
//       vesselTm: vesselTmWS,
//       rocketStatus: rocketStatusWS,
//       flightEventRecord: flightEventRecordWS,
//     };

//     const websocket = websockets[endpoint];
//     if (websocket) {
//       websocket.send(message);
//     }
//   };

//   const value = {
//     sendMessage,
//     messages: {
//       vesselTm: vesselTmData,
//       rocketStatus: rocketStatusData,
//       flightEventRecord: flightEventRecordData,
//     },
//   };

//   return (
//     <WebSocketContext.Provider value={value}>
//       {children}
//     </WebSocketContext.Provider>
//   );
// };
