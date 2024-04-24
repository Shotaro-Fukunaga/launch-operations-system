import { BasicLayout } from "../../../components/Layout/BasicLayout";
import { TimelineBar } from "../components/VerticalTimeLine/TimelineBar";
import { FlightVisualizer } from "../components/FlightVisual/FlightVisualizer";
import { LivePlayer } from "../../../components/Live/LivePlayer";
import CesiumComponent from "../../../components/Cesium/Cesium";
import { WebSocketContext } from "../../../context/WebSocketContext";
import { useContext, useState, useEffect } from "react";
// 後日しっかりと作る
import { DynamicLineChart } from "../../../components/Chart/AltitudeGraph";
import React from "react";
import TerminalLog from "../../../components/Terminal/TerminalLog";

function getTimeStrings(minutes: number): string[] {
  // 現在の日時を取得
  const currentTime = new Date();

  // 結果を格納する配列
  const timeStrings: string[] = [];

  // 指定された分数の秒数
  const totalSeconds = minutes * 60;

  for (let i = 0; i <= totalSeconds; i++) {
    // 現在の時間にi秒を加算
    const newTime = new Date(currentTime.getTime() + i * 1000);

    // 時間を "hh:mm:ss" の形式で文字列化して配列に追加
    timeStrings.push(newTime.toTimeString().substring(0, 8));
  }

  return timeStrings;
}

export const LaunchDataViewer = React.memo(() => {
  const webSocketContext = useContext(WebSocketContext);
  const [altitudeData, setAltitudeData] = useState<number[]>([]);
  const labels: string[] = getTimeStrings(8);

  useEffect(() => {
    if (!webSocketContext) {
      return;
    }

    const { messages } = webSocketContext;
    const { surfaceInfo } = messages;
    const rawAltitude = surfaceInfo["altitude_als"];

    let newAltitude = Number(rawAltitude);

    if (isNaN(newAltitude)) return;
    newAltitude = parseFloat(newAltitude.toFixed(2));

    // 高度データとラベルを更新
    setAltitudeData((oldData) => {
      const lastAltitude = oldData[oldData.length - 1];
      if (lastAltitude === newAltitude) {
        return oldData; // 前のデータと同じ場合は更新しない
      }
      return [...oldData, newAltitude];
    });
  }, [webSocketContext]);

  if (!webSocketContext) {
    return <div>Loading...</div>;
  }
  const { messages } = webSocketContext;
  const { orbitInfo, surfaceInfo } = messages;

  const displayData = [
    { label: "高度", value: surfaceInfo["altitude_als"], unit: "m" },
    { label: "遠点高度", value: orbitInfo["apoapsis_altitude"], unit: "m" },
    { label: "近点高度", value: orbitInfo["periapsis_altitude"], unit: "m" },
    { label: "軌道速度", value: orbitInfo["orbital_speed"], unit: "m/s" },
    { label: "表面速度", value: surfaceInfo["surface_speed"], unit: "m/s" },
    { label: "垂直速度", value: surfaceInfo["vertical_speed"], unit: "m/s" },
    { label: "軌道傾斜角", value: orbitInfo["inclination"], unit: "°" },
    { label: "軌道離心率", value: orbitInfo["eccentricity"], unit: "" },
    { label: "進行方向", value: surfaceInfo["heading"], unit: "°" },
  ];

  // backエンドで丸め込む
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const formatValue = (value: any, unit: string) => {
    const formattedValue = isNaN(value) ? value : Number(value).toFixed(2);
    return `${formattedValue} ${unit}`.trim();
  };

  return (
    <BasicLayout>
      <div className="flex flex-wrap h-full">
        <div className="flex h-[55%] w-full">
          <div className="border border-gray-500 w-[20%] h-full bg-[#242424]">
            {/* Altitude Graph */}
            <div className="h-[65%] w-full overflow-x-scroll">
              <DynamicLineChart
                labels={labels}
                chartTitle="上昇ステータス"
                datasetLabel="高度 (m)"
                data={altitudeData}
                fillColor="rgba(75, 192, 192, 0.1)"
                borderColor="rgba(75, 192, 192, 0.6)"
                xGridColor="rgba(255, 99, 132, 0.2)"
                yGridColor="rgba(255, 99, 132, 0.2)"
              />
            </div>
            {/* Flight Status */}
            <div className="h-[40%] px-[1rem] text-[0.8rem]">
              {displayData.map((item, index) => (
                <p key={index} className="text-white">
                  {item.label}: {formatValue(item.value, item.unit)}
                </p>
              ))}
            </div>
          </div>

          {/* 軌道の表示 */}
          <div className="border border-gray-500 w-[60%] h-full">
            <CesiumComponent />
          </div>

          {/* 進行中のタスク */}
          <div className="w-[20%] h-full bg-[#242424]">
            <TimelineBar
              events={[
                { time: "13:00", name: "LIFT OFF", color: "green" },
                { time: "16:00", name: "MECO", color: "green" },
                { time: "16:18", name: "HOGE", color: "yellow" },
                { time: "21:18", name: "HOGE", color: "red" },
              ]}
            />
          </div>
        </div>

        <div className="flex h-[45%] w-full border border-gray-500">
          <div className="w-[65%] h-full flex bg-gray-200">
            <div className="w-[25%] ">
              <TerminalLog logs={[]} />
            </div>
            <div className="w-[35%]">{/* お天気の情報 */}</div>
            <div className="w-[40%]">
              <FlightVisualizer />
            </div>
          </div>
          <div className="w-[35%] h-full  flex justify-center">
            <LivePlayer />
          </div>
        </div>
      </div>
    </BasicLayout>
  );
});
