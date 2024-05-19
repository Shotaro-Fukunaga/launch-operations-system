import React, { useState, useEffect } from "react";

type LaunchTimerProps = {
  launchTime: Date;
  launchRelativeTime?: number;
};

const LaunchTimer: React.FC<LaunchTimerProps> = ({
  launchTime,
  launchRelativeTime,
}) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timerId = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000); // 1秒ごとに現在時刻を更新

    return () => clearInterval(timerId); // コンポーネントのクリーンアップ
  }, []);

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

  const utcTime = currentTime.toISOString().slice(0, 19).replace("T", " ");
  const jstTime = new Date(currentTime.getTime() + 9 * 3600000)
    .toISOString()
    .slice(0, 19)
    .replace("T", " ");
  return (
    <div className="flex flex-col">
      <div className="w-full flex justify-center gap-[1rem]">
        <p className="text-[1.8rem]">
          {formatRelativeTime(launchRelativeTime)}
        </p>
        <div className="flex flex-col">
          <p className="text-[0.8rem]">UTC {utcTime}</p>
          <p className="text-[0.8rem]">JST {jstTime}</p>
        </div>
      </div>
      <div className="flex justify-center w-full">
        <p className="text-[1.2rem]">
          Launch time {launchTime.toISOString().slice(0, 16).replace("T", " ")}
        </p>
      </div>
    </div>
  );
};

export default LaunchTimer;
