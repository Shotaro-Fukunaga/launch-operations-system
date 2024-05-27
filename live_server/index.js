const NodeMediaServer = require('node-media-server');
const ffmpeg = require('@ffmpeg-installer/ffmpeg');

const config = {
  rtmp: {
    port: 1935, // RTMPサーバーのポート番号
    chunk_size: 60000, // RTMPのチャンクサイズ（単位はバイト）
    gop_cache: false, // GOPキャッシュを無効にして、遅延を減らす設定
    ping: 30, // RTMPのピング間隔（秒）
    ping_timeout: 60, // RTMPのタイムアウト設定（秒）
  },
  http: {
    port: 8010, // HTTPサーバーのポート番号
    mediaroot: './media', // メディアファイルのルートディレクトリ
    allow_origin: '*', // CORSポリシー、全てのドメインからのアクセスを許可
  },
  trans: {
    ffmpeg: ffmpeg.path, // FFmpegのパス
    tasks: [
      {
        app: 'live', // アプリケーション名（ストリーミング識別子）
        hls: true, // HLSでのストリーミングを有効にする
        rtmp: true, // RTMPでのストリーミングを有効にする
        dash: false, // DASH設定を無効にし、このフォーマットでの配信を行わない
        vc: "h264_nvenc", // NVIDIA GPUを使ったH264エンコーディングを使用
        ac: "copy", // オーディオは再エンコードせずにコピーする
        vcParams: [
          '-preset', 'ultrafast',
          '-tune', 'zerolatency',
          '-g', '12',
          '-keyint_min', '12',
          '-sc_threshold', '0',
          '-b:v', '2000k',
          '-maxrate', '2000k',
          '-bufsize', '4000k'
        ],
        acParams: [
          '-b:a', '128k',
          '-ac', '2', 
          '-ar', '48000'
        ],
        hlsFlags: '[hls_time=0.05:hls_list_size=3:hls_flags=delete_segments+append_list]'
      }
    ]
  }
};

var nms = new NodeMediaServer(config);
nms.run();