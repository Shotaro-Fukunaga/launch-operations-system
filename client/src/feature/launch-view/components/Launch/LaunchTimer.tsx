import React, { useState, useEffect } from 'react';

type LaunchTimerProps = {
  launchTime: Date; // launchTime を Date 型で受け取る
  launchRelativeTime?: string;
};

const LaunchTimer: React.FC<LaunchTimerProps> = ({ launchTime,launchRelativeTime }) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timerId = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000); // 1秒ごとに現在時刻を更新

    return () => clearInterval(timerId); // コンポーネントのクリーンアップ
  }, []);

  const utcTime = currentTime.toISOString().slice(0, 19).replace('T', ' ');
  const jstTime = new Date(currentTime.getTime() + 9 * 3600000).toISOString().slice(0, 19).replace('T', ' ')
  return (
    <div className="flex flex-col">
      <div className="w-full flex justify-center gap-[1rem]">
        <p className="text-[1.8rem]">{launchRelativeTime?.replace('T', 'X') ?? "X - 00:00:00"}</p>
        <div className="flex flex-col">
          <p className="text-[0.8rem]">UTC {utcTime}</p>
          <p className="text-[0.8rem]">JST {jstTime}</p>
        </div>
      </div>
      <div className="flex justify-center w-full">
        <p className="text-[1.2rem]">Launch time {launchTime.toISOString().slice(0, 16).replace('T', ' ')}</p>
      </div>
    </div>
  );
};

export default LaunchTimer;
