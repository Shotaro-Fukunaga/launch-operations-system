import React, { useEffect, useRef } from "react";
import { EventRecord } from "../../types/flightRecordType";

interface TerminalLogProps {
  logs?: EventRecord[]; // logs は undefined を許容する
}

const TerminalLog: React.FC<TerminalLogProps> = ({ logs }) => {
  const endOfLogsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (endOfLogsRef.current) {
      endOfLogsRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  const formatTime = (timeString: string) => {
    const [date, time] = timeString.split('T');
    const [hours, minutes, seconds] = time.split('.')[0].split(':');
    return `${date} ${hours}:${minutes}:${seconds}`;
  };

  const renderContent = () => {
    if (!logs || logs.length === 0) {
      return (
        <div className="text-white text-[0.8rem]">Terminal Standby ...</div>
      );
    }
    return logs.map((log, index) => (
      <div key={index} className="text-blue-300 text-[0.8rem]">
        {formatTime(log.time)} - {log.level} - {log.msg}
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
