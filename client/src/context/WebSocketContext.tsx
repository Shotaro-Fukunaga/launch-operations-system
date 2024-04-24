import React, { createContext, useState, useEffect, ReactNode } from "react";

type TelemetryType = { [key: string]: string | number | string | number[] };

export type WebSocketContextType = {
  sendMessage: (endpoint: string, message: string) => void;
  messages: {
    atmosphereInfo: TelemetryType;
    orbitInfo: TelemetryType;
    surfaceInfo: TelemetryType;
    deltaVStatus: TelemetryType;
    thermalStatus: TelemetryType;
    satelliteBusStatus: TelemetryType;
    communicationStatus: TelemetryType;
  };
};
type WebSocketProviderProps = {
  children: ReactNode;
};

export const WebSocketContext = createContext<WebSocketContextType | null>(
  null
);

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
}) => {
  const [atmosphereInfoMessage, setAtmosphereInfoMessage] =
    useState<TelemetryType>({});
  const [orbitInfoMessage, setOrbitInfoMessage] = useState<TelemetryType>({});
  const [deltaVStatusMessage, setDeltaVStatusMessage] = useState<TelemetryType>(
    {}
  );
  const [surfaceInfoMessage, setSurfaceInfoMessage] = useState<TelemetryType>(
    {}
  );
  const [thermalStatusMessage, setThermalStatusMessage] =
    useState<TelemetryType>({});
  const [satelliteBusStatusMessage, setSatelliteBusStatusMessage] =
    useState<TelemetryType>({});
  const [communicationStatusMessage, setCommunicationStatusMessage] =
    useState<TelemetryType>({});

  const [orbitInfoWS, setOrbitInfoWS] = useState<WebSocket | null>(null);
  const [surfaceInfoWS, setSurfaceInfoWS] = useState<WebSocket | null>(null);
  const [deltaVStatusWS, setDeltaVStatusWS] = useState<WebSocket | null>(null);
  const [thermalStatusWS, setThermalStatusWS] = useState<WebSocket | null>(
    null
  );
  const [atmosphereInfoWS, setAtmosphereInfoWS] = useState<WebSocket | null>(
    null
  );
  const [satelliteBusStatusWS, setSatelliteBusStatusWS] =
    useState<WebSocket | null>(null);
  const [communicationStatusWS, setCommunicationStatusWS] =
    useState<WebSocket | null>(null);

  useEffect(() => {
    const endpoints = [
      {
        url: "ws://localhost:8000/ws/atmosphere_info",
        setWs: setAtmosphereInfoWS,
        setMessage: setAtmosphereInfoMessage,
      },
      {
        url: "ws://localhost:8000/ws/orbit_info",
        setWs: setOrbitInfoWS,
        setMessage: setOrbitInfoMessage,
      },
      {
        url: "ws://localhost:8000/ws/surface_info",
        setWs: setSurfaceInfoWS,
        setMessage: setSurfaceInfoMessage,
      },
      {
        url: "ws://localhost:8000/ws/delta_v_status",
        setWs: setDeltaVStatusWS,
        setMessage: setDeltaVStatusMessage,
      },
      {
        url: "ws://localhost:8000/ws/thermal_status",
        setWs: setThermalStatusWS,
        setMessage: setThermalStatusMessage,
      },
      {
        url: "ws://localhost:8000/ws/satellite_bus_status",
        setWs: setSatelliteBusStatusWS,
        setMessage: setSatelliteBusStatusMessage,
      },
      {
        url: "ws://localhost:8000/ws/communication_status",
        setWs: setCommunicationStatusWS,
        setMessage: setCommunicationStatusMessage,
      },
    ];

    endpoints.forEach(({ url, setWs, setMessage }) => {
      const websocket = new WebSocket(url);
      websocket.onopen = () => {
        console.log(`Connected to ${url}`);
        setWs(websocket);
      };
      websocket.onmessage = (evt) => {
        try {
          const data = JSON.parse(evt.data);
          // console.log(`Data received from ${url}:`, data);
          setMessage(data);
        } catch (error) {
          console.error("Error parsing JSON!", error);
        }
      };
      websocket.onclose = () => {
        console.log(`Disconnected from ${url}`);
        setWs(null);
      };
    });

    return () => {
      endpoints.forEach(({ setWs }) => {
        setWs((ws) => {
          if (ws) ws.close();
          return null;
        });
      });
    };
  }, []);

  const sendMessage = (endpoint: string, message: string) => {
    const websockets: { [key: string]: WebSocket | null } = {
      atmosphereInfo: atmosphereInfoWS,
      orbitInfo: orbitInfoWS,
      surfaceInfo: surfaceInfoWS,
      deltaVStatus: deltaVStatusWS,
      thermalStatus: thermalStatusWS,
      satelliteBusStatus: satelliteBusStatusWS,
      communicationStatus: communicationStatusWS,
    };

    const websocket = websockets[endpoint];
    if (websocket) {
      websocket.send(message);
    }
  };

  const value = {
    sendMessage,
    messages: {
      atmosphereInfo: atmosphereInfoMessage,
      orbitInfo: orbitInfoMessage,
      surfaceInfo: surfaceInfoMessage,
      deltaVStatus: deltaVStatusMessage,
      thermalStatus: thermalStatusMessage,
      satelliteBusStatus: satelliteBusStatusMessage,
      communicationStatus: communicationStatusMessage,
    },
  };

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  );
};
