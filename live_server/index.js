const NodeMediaServer = require('node-media-server');
const config = {
  rtmp: {
    port: 1935,
    chunk_size: 60000,
    gop_cache: false, // GOPキャッシュを無効にしてリアルタイム性を向上
    ping: 30,
    ping_timeout: 60,
  },
  http: {
    port: 8000,
    mediaroot: './media',
    allow_origin: '*',
  },
  trans: {
    ffmpeg: '/opt/homebrew/bin/ffmpeg',
    tasks: [
      {
        app: 'live',
        hls: true,
        // hls_timeを1秒未満に設定することでセグメントの長さを短くし、遅延を減らす
        // hls_list_sizeを小さくすることで、クライアントがダウンロードするプレイリストのサイズを小さくし、遅延を減らす
        hlsFlags: '[hls_time=0.5:hls_list_size=2:hls_flags=delete_segments]',
        dash: false, // DASHは低遅延には適していないため無効にする
      },
    ],
  },
};

var nms = new NodeMediaServer(config);
nms.run();