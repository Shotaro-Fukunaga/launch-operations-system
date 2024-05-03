import { BasicLayout } from "../../../components/Layout/BasicLayout";
import { FlightVisualizer } from "../components/FlightVisual/FlightVisualizer";
import { LivePlayer } from "../../../components/Live/LivePlayer";
import CesiumComponent from "../../../components/Cesium/Cesium";
import { useContext } from "react";
import React from "react";
import TerminalLog from "../../../components/Terminal/TerminalLog";
import { WebSocketContext } from "../../../context/WebSocketContext";
import WeatherInfo from "../../../components/WeatherInfo";
import VesselTelemetryViewer from "../components/VesselTelemetryViewer";
import RealTimeChart from "../../../components/Chart/RealTimeChart";
import LaunchScreen from "../components/Launch/LaunchScreen";

export const LaunchDataViewer = React.memo(() => {
  const webSocketContext = useContext(WebSocketContext);

  if (!webSocketContext) {
    return <div>Loading...</div>;
  }
  const { messages } = webSocketContext;
  const { flightEventRecord, vesselTm } = messages;
  const orbitInfo = vesselTm?.orbit_info;

  return (
    <BasicLayout>
      <div className="flex flex-wrap w-full h-full">
        {/* ################################ 上半分 ################################ */}
        <div className="flex h-[60%] w-full">

          
          <div className="w-[20%] h-full bg-[#242424] flex-col">
            <div className="h-[50%] w-full text-white">
              <LaunchScreen orbitInfo={orbitInfo} />
            </div>

            <div className="w-full h-[50%] bg-[#242424]">
              <TerminalLog logs={flightEventRecord?.event_records} />
            </div>
          </div>

          <div className="border border-gray-500 w-[56%] h-full">
            <CesiumComponent
              flightRecords={flightEventRecord?.flight_records ?? []}
            />
          </div>

          <div className="w-[24%] h-full bg-[#242424] text-white">
            <FlightVisualizer />
          </div>
        </div>

        {/* ################################ 下半分 ################################ */}

        <div className="flex h-[40%] w-full border border-gray-500">
          <div className="w-[35%] h-full flex bg-gray-200">
            <RealTimeChart
              data={flightEventRecord?.flight_records ?? []}
              attributeKey="altitude"
              attributeName="Altitude (m)"
            />
          </div>
          <div className="w-[15%] h-full bg-gray-200 border border-gray-300">
            <VesselTelemetryViewer telemetryData={vesselTm} />
          </div>
          <div className="w-[15%] h-full">
            <WeatherInfo />
          </div>
          <div className="w-[35%] h-full  flex justify-center">
            <LivePlayer />
          </div>
        </div>
      </div>
    </BasicLayout>
  );
});
