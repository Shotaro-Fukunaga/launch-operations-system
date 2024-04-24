// TerminalLog.tsx
import React from "react";

export interface Log {
  timestamp: string;
  type: "error" | "warning" | "info";
  text: string;
}
// propsの型を定義
interface TerminalLogProps {
  logs: Log[];
}

const TerminalLog: React.FC<TerminalLogProps> = ({ logs }) => {
  const renderLog = (log: Log, index: number) => {
    let color;
    switch (log.type) {
      case "error":
        color = "text-red-500";
        break;
      case "warning":
        color = "text-yellow-500";
        break;
      default:
        color = "text-green-500";
    }

    return (
      <div key={index} className={`${color}`}>
        {`${log.timestamp} - ${log.text}`}
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
