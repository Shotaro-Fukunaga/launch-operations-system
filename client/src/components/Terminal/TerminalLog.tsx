import React from "react";
import { EventRecord } from "../../types/flightRecordType";

interface TerminalLogProps {
  logs: EventRecord[];
}

const TerminalLog: React.FC<TerminalLogProps> = ({ logs }) => {
  const renderLog = (log: EventRecord, index: number) => {
    let color;
    let logType = "info"; // デフォルトはinfoとする

    switch (log.event_level) {
      case 2: // エラーレコード
        color = "text-red-500";
        logType = "error";
        break;
      case 1: // 重要なレコード
        color = "text-yellow-500";
        logType = "warning";
        break;
      default: // 通常のレコード
        color = "text-green-500";
    }

    return (
      <div key={index} className={`${color}`}>
        {`${log.time} [${logType.toUpperCase()}] - ${log.event_details}`}
      </div>
    );
  };

  return (
    <div className="w-full h-full p-3 overflow-y-auto text-white bg-black">
      {logs.map(renderLog)}
    </div>
  );
};

export default TerminalLog;
