import React, { useEffect, useRef } from "react";
import { EventRecord } from "../types/flightRecordType";

type Props = {
  logs?: EventRecord[];
}

const TerminalLog: React.FC<Props> = ({ logs }) => {
  const endOfLogsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (endOfLogsRef.current) {
      endOfLogsRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  const formatRelativeTime = (relativeTime: number | undefined) => {
    if (relativeTime === undefined) return "X - 00:00:00";

    const sign = relativeTime < 0 ? "-" : "+";
    const absTime = Math.abs(relativeTime);
    const hours = Math.floor(absTime / 3600)
      .toString()
      .padStart(2, "0");
    const minutes = Math.floor((absTime % 3600) / 60)
      .toString()
      .padStart(2, "0");
    const seconds = (absTime % 60).toString().padStart(2, "0");

    return `X ${sign} ${hours}:${minutes}:${seconds}`;
  };

  const renderContent = () => {
    if (!logs || logs.length === 0) {
      return (
        <div className="text-white text-[0.8rem]">Terminal Standby ...</div>
      );
    }
    return logs.map((log, index) => (
      <div key={index} className="text-blue-300 text-[0.8rem]">
        {formatRelativeTime(log.launch_relative_time)} : {log.event}
      </div>
    ));
  };

  return (
    <div className="relative w-full h-full shadow-md">
      <div className="h-[8%] text-white text-[1rem] w-full bg-gray-600 shadow-md flex justify-center">
        Flight Event Log
      </div>
      <div className="h-[92%] w-full overflow-y-auto pl-[0.6rem] py-[0.4rem]">
        {renderContent()}
        <div ref={endOfLogsRef} />
      </div>
    </div>
  );
};

export default TerminalLog;
