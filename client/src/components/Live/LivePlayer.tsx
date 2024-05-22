import { useEffect, useRef } from "react";
import ReactPlayer from "react-player";

export const LivePlayer = () => {
  const playerRef = useRef(null);

  // 再生位置を調整する関数
  // const handleSeekToEnd = () => {
  //   const player = playerRef.current as ReactPlayer | null;
  //   if (player && player.getDuration) {
  //     const duration = player.getDuration();
  //     player.seekTo(duration-1, "seconds");
  //   }
  // };

  // useEffect(() => {
  //   // コンポーネントがマウントされたらすぐに最新位置にシークする
  //   handleSeekToEnd();

  //   const interval = setInterval(() => {
  //     handleSeekToEnd();
  //   }, 10000);

  //   // コンポーネントがアンマウントされるときにインターバルをクリアする
  //   return () => clearInterval(interval);
  // }, []);

  return (
    <div className="player-wrapper">
      <ReactPlayer
        ref={playerRef}
        // TODO 環境変数から取得する
        url="http://localhost:8010/live/ksp/index.m3u8"
        width="100%"
        height="100%"
        controls={true}
        playing={true}
        muted={true}
        // onReady={handleSeekToEnd}
        config={{
          file: {
            forceHLS: true,
            attributes: {
              preload: 'auto',
              autoPlay: true,
              controls: true,
              muted: true
            },
            hlsOptions: {
              liveSyncDurationCount: 1,
              lowLatencyMode: true,
              initialLiveManifestSize: 1,
              maxBufferLength: 1,
              maxMaxBufferLength: 1,
              maxBufferSize: 10 * 1000 * 1000,
              maxBufferHole: 0.05
            }
          }
        }}
      />
    </div>
  );
};
