import React, { useEffect, useRef, useState } from "react";
import { EventRecord } from "../../types/flightRecordType";

interface TerminalLogProps {
  logs: EventRecord[];
}

const TerminalLog: React.FC<TerminalLogProps> = ({ logs }) => {
  const [showTime, setShowTime] = useState(true);
  const endOfLogsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // logsが更新されるたびに最新のログにスクロールする
    if (endOfLogsRef.current) {
      endOfLogsRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  const renderLog = (log: EventRecord, index: number) => {
    let color;
    let logType = "info"; // デフォルトはinfoとする

    switch (log.event_level) {
      case 2: // エラーレコード
        color = "text-red-500";
        logType = "error";
        break;
      case 1: // 重要なレコード
        color = "text-green-500";
        logType = "info";
        break;
      default: // 通常のレコード
        color = "text-white";
    }

    const date = new Date(log.time);
    const formattedDate = date.toLocaleDateString("ja-JP"); // "yyyy/mm/dd" 形式

    return (
      <div key={index} className={`${color}`}>
        {showTime ? `` : formattedDate} [{logType.toUpperCase()}] -{" "}
        {log.event_details}
      </div>
    );
  };

  return (
    <div className="w-full h-full bg-black relative pl-[0.6rem] py-[0.4rem]">
      <button
        onClick={() => setShowTime(!showTime)}
        className="p-2 text-[0.6rem] text-white bg-gray-800 hover:bg-gray-600 absolute flex justify-end right-6 top-2 z-10"
      >
        {showTime ? "Hide Time" : "Show Time"}
      </button>

      <div className="h-full w-full overflow-y-auto">
        {logs.map(renderLog)}
        <div ref={endOfLogsRef} />
      </div>
    </div>
  );
};

export default TerminalLog;
