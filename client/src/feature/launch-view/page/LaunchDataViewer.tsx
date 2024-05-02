import { BasicLayout } from "../../../components/Layout/BasicLayout";
import { TimelineBar } from "../components/VerticalTimeLine/TimelineBar";
import { FlightVisualizer } from "../components/FlightVisual/FlightVisualizer";
import { LivePlayer } from "../../../components/Live/LivePlayer";
import CesiumComponent from "../../../components/Cesium/Cesium";
import { useContext } from "react";
import { DynamicLineChart } from "../../../components/Chart/AltitudeGraph";
import React from "react";
import TerminalLog from "../../../components/Terminal/TerminalLog";
import { WebSocketContext } from "../../../context/WebSocketContext";

export const LaunchDataViewer = React.memo(() => {
  const webSocketContext = useContext(WebSocketContext);

  if (!webSocketContext) {
    return <div>Loading...</div>;
  }
  const { messages } = webSocketContext;
  const { flightEventRecord } = messages;

  return (
    <BasicLayout>
      <div className="flex h-full">
        <div className="w-[20%] h-full flex flex-col ">
          <div className="h-[40%] w-full bg-[#242424]">
            <div>
              <h1>Flight Manager</h1>
              {/* <button onClick={connect}>Connect</button>
              <button onClick={disconnect}>Disconnect</button>
              <button onClick={() => sendMessage({ action: "start" })}>
                Start Mission
              </button>
              <h2>Flight Records</h2> */}
              {/* <ul>
                {flightRecords.map((record, index) => (
                    <li key={index}>{JSON.stringify(record)}</li>
                ))}
            </ul>
            <h2>Event Records</h2>
            <ul>
                {eventRecords.map((record, index) => (
                    <li key={index}>{JSON.stringify(record)}</li>
                ))}
            </ul> */}
            </div>
          </div>
          <div className="h-[60%] w-full">
            <FlightVisualizer />
          </div>
        </div>

        <div className="w-[80%] h-full flex flex-wrap">
          <div className="flex h-[55%] w-full">
            {/* 軌道の表示 */}
            <div className="border border-gray-500 w-[80%] h-full">
              <CesiumComponent
                flightRecords={flightEventRecord?.flight_records ?? []}
              />
            </div>

            {/* 進行中のタスク */}
            <div className="w-[20%] h-full bg-[#242424]">
              <TimelineBar events={flightEventRecord?.event_records ?? []} />
            </div>
          </div>

          <div className="flex h-[45%] w-full border border-gray-500">
            <div className="w-[60%] h-full flex bg-gray-200">
              <div className="w-[70%]">
                <DynamicLineChart
                  labels={["1", "2", "3", "4", "5", "6", "7", "8"]}
                  chartTitle="上昇ステータス"
                  datasetLabel="高度 (m)"
                  data={[100, 200, 300, 400, 500, 600, 700, 800]}
                  fillColor="rgba(75, 192, 192, 0.1)"
                  borderColor="rgba(75, 192, 192, 0.6)"
                  xGridColor="rgba(255, 99, 132, 0.2)"
                  yGridColor="rgba(255, 99, 132, 0.2)"
                />
              </div>
              <div className="w-[30%] ">
                <TerminalLog logs={flightEventRecord?.event_records ?? []} />
              </div>
            </div>
            <div className="w-[40%] h-full  flex justify-center">
              <LivePlayer />
            </div>
          </div>
        </div>
      </div>
    </BasicLayout>
  );
});
