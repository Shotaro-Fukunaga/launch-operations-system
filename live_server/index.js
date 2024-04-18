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
          '-preset', 'llhp',       // エンコーダーのプリセットとして低遅延高性能を指定
          '-profile:v', 'main',    // H264のプロファイルをmainに設定
          '-rc:v', 'vbr_hq',       // 可変ビットレートで高品質を指定
          '-cq:v', '19',           // 品質基準値（低いほど高品質）
          '-b:v', '1500k',         // ビデオビットレートの基本値
          '-maxrate:v', '2000k',   // ビデオの最大ビットレート
          '-bufsize:v', '5000k',   // ビットレート制御のバッファサイズ
        ],
        acParams: [
          '-b:a', '128k',         // オーディオビットレート
          '-ac', '2',             // オーディオのチャンネル数
          '-ar', '48000'          // オーディオのサンプルレート（Hz）
        ],
        hlsFlags: '[hls_time=0.5:hls_list_size=2:hls_flags=delete_segments+append_list]' // HLSストリーミングの具体的なフラグ設定
      }
    ]
  }
};

var nms = new NodeMediaServer(config);
nms.run();