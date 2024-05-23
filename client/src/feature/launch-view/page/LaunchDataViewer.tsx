import { BasicLayout } from "../../../components/Layout/BasicLayout";
import { FlightVisualizer } from "../components/FlightVisual/FlightVisualizer";
import { LivePlayer } from "../../../components/Live/LivePlayer";
import CesiumComponent from "../../../components/Cesium/Cesium";
import { useEffect, useState } from "react";
import React from "react";
import TerminalLog from "../../../components/Terminal/TerminalLog";
import WeatherInfo from "../../../components/WeatherInfo";
import VesselTelemetryViewer from "../components/VesselTelemetryViewer";
import RealTimeChart from "../../../components/Chart/RealTimeChart";
import LaunchScreen from "../components/Launch/LaunchScreen";
import { EventRecord, FlightRecord } from "../../../types/flightRecordType";
import { VesselTelemetryType } from "../../../types/vesselTelemetryType";
import { RocketStatusType } from "../../../types/rocketStatusType";

interface TelemetryData {
  time?: string;
  launch_relative_time?: number;
  flight_records?: FlightRecord[];
  event_records?: EventRecord[];
  rocket_status?: RocketStatusType;
  vessel_telemetry?: VesselTelemetryType;
}

export const LaunchDataViewer = React.memo(() => {
  const [webSocket, setWebSocket] = useState<WebSocket | null>(null);
  const [telemetryData, setTelemetryData] = useState<TelemetryData>({});

  useEffect(() => {
    // WebSocket 接続を開設
    const ws = new WebSocket("ws://localhost:8000/ws/launch-management");
    ws.onopen = () => {
      console.log("WebSocket Connected");
    };
    ws.onmessage = (event: MessageEvent) => {
      try {
        const data: TelemetryData = JSON.parse(event.data);
        setTelemetryData(data);
      } catch (err) {
        console.error("Error parsing data", err);
      }
    };
    ws.onerror = (event: Event) => {
      console.error("WebSocket Error", event);
    };
    ws.onclose = () => {
      console.log("WebSocket Disconnected");
    };

    setWebSocket(ws);

    // WebSocket 接続をクリーンアップ
    return () => {
      ws.close();
    };
  }, []);

  const sendCommand = (command: object): void => {
    if (webSocket && webSocket.readyState === WebSocket.OPEN) {
      webSocket.send(JSON.stringify(command));
    }
  };

  const flightRecord = telemetryData.flight_records;
  const eventRecord = telemetryData.event_records;
  const vesselTm = telemetryData.vessel_telemetry;
  const rocketStatus = telemetryData.rocket_status;

  return (
    <BasicLayout>
      <div className="flex flex-wrap w-full h-full bg-[#242424] text-white">
        {/* ################################ 上半分 ################################ */}
        <div className="flex h-[60%] w-full">
          <div className="w-[20%] h-full flex-col">
            <div className="h-[50%] w-full text-white">
              <LaunchScreen
                orbitInfo={vesselTm?.orbit_info}
                launchRelativeTime={telemetryData.launch_relative_time}
                sendCommand={sendCommand}
              />
            </div>

            <div className="w-full h-[50%] bg-[#242424]">
              <TerminalLog logs={eventRecord ?? []} />
            </div>
          </div>

          <div className="border-l border-r border-gray-500 w-[56%] h-full">
            <CesiumComponent flightRecords={flightRecord ?? []} />
          </div>

          <div className="w-[24%] h-full bg-[#242424] text-white">
            <FlightVisualizer rocketStatus={rocketStatus} />
          </div>
        </div>

        {/* ################################ 下半分 ################################ */}

        <div className="flex h-[40%] w-full border-t border-gray-500">
          <div className="w-[36%] h-full ">
            <RealTimeChart
              data={flightRecord ?? []}
              attributeKey="altitude"
              attributeName="Altitude (m)"
            />
          </div>
          <div className="w-[15%] h-full border-l border-gray-500">
            <VesselTelemetryViewer telemetryData={vesselTm} />
          </div>
          <div className="w-[15%] h-full border-l border-r border-gray-500">
            <WeatherInfo />
          </div>
          <div className="w-[34%] h-full flex justify-center">
            <LivePlayer />
          </div>
        </div>
      </div>
    </BasicLayout>
  );
});
