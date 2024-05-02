import { useState, useEffect, FC, useRef } from "react";
import MarkerGenerator from "./MarkerGenerator";
import { EventMarkerGenerator } from "./EventMarkerGenerator";
import { Countdown } from "./Countdown";
import { EventRecord } from "../../../../types/flightRecordType";

// 現在時刻の位置を計算
const calculateCurrentTimePosition = () => {
  const now = new Date();
  const secondsSinceMidnight =
    now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds();
  return (secondsSinceMidnight / (24 * 3600)) * 100;
};

type Props = {
  events?: EventRecord[];
};

export const TimelineBar: FC<Props> = ({ events }) => {
  const [isAutoScrollEnabled, setIsAutoScrollEnabled] = useState(true); // 自動スクロールが有効かどうかを追跡
  const [currentTimePosition, setCurrentTimePosition] = useState(
    calculateCurrentTimePosition()
  );

  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const userScrollActivityRef = useRef(false);

  // スクロールイベントハンドラー
  const handleUserScroll = () => {
    userScrollActivityRef.current = true; // ユーザーによるスクロール操作を検出
    setIsAutoScrollEnabled(false); // 自動スクロールを無効化
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTimePosition(calculateCurrentTimePosition());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // スクロールコンテナにイベントリスナーを追加
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (container) {
      container.addEventListener("scroll", handleUserScroll);

      return () => {
        container.removeEventListener("scroll", handleUserScroll);
      };
    }
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      if (!userScrollActivityRef.current) {
        // ユーザーのスクロール操作がなければ自動スクロール
        setIsAutoScrollEnabled(true);
        const newPosition = calculateCurrentTimePosition();
        setCurrentTimePosition(newPosition);

        if (isAutoScrollEnabled && scrollContainerRef.current) {
          const container = scrollContainerRef.current;
          const scrollHeight = container.scrollHeight;
          const height = container.clientHeight;
          const scrollPosition = (newPosition / 100) * scrollHeight;

          container.scrollTop = scrollPosition - height / 2;
        }
      }
      userScrollActivityRef.current = false; // ユーザー操作フラグをリセット
    }, 1000);

    return () => clearInterval(timer);
  }, [isAutoScrollEnabled]);

  return (
    <div className="h-full w-full relative">
      <div className="w-full absolute flex justify-end px-[1rem] z-[1000]">
        <div className="w-[70%] text-white text-[0.8rem] bg-black bg-opacity-40">
          {/* TODO リフトオフ時間 */}
          <Countdown launchDateTime={new Date(2024, 2, 16, 17, 0, 0)} />
        </div>
      </div>
      <div
        className="overflow-auto overflow-x-hidden h-full w-full pl-[4rem]"
        ref={scrollContainerRef}
      >
        {/* スクロールするマーカーと現在時刻のポジションを表示するコンテナ */}
        <div className="relative h-[1500rem]">
          <MarkerGenerator />

          {/* ロケットのイベントマーカー */}
          <EventMarkerGenerator events={events} />

          <div
            className="transition-height duration-500 absolute w-1 bg-white rounded-full"
            style={{ height: `${currentTimePosition}%`, zIndex: 3 }}
          />
        </div>
      </div>
      {/* グレーの背景ライン */}
      <div
        className="absolute h-full w-1 bg-gray-600"
        style={{ top: 0, left: "4rem" }}
      />
    </div>
  );
};
