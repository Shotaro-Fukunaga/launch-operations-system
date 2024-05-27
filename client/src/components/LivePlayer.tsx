import { useRef } from "react";
import ReactPlayer from "react-player";

export const LivePlayer = () => {
  const playerRef = useRef(null);
  return (
    <div className="player-wrapper">
      <ReactPlayer
        ref={playerRef}
        url="http://localhost:8010/live/ksp/index.m3u8"
        width="100%"
        height="100%"
        controls={true}
        playing={true}
        muted={true}
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
