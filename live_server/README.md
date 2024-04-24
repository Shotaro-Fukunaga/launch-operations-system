
# Live Streaming Server with NodeMediaServer

## 必要条件

- Node.js（バージョン10以降を推奨）

## 依存関係をインストール




   ```bash
   npm install
   ```


## 設定

ストリーミングサーバーの設定は、Node.jsスクリプト内の `config` オブジェクトで定義されています。以下は設定パラメータの詳細です：

- **RTMP設定**：
  - `port`: RTMPサーバーがリッスンするポート番号。
  - `chunk_size`: RTMPのデータチャンクサイズ（バイト単位）。
  - `gop_cache`: 遅延を減らすために無効化。
  - `ping` と `ping_timeout`: ネットワークチェック設定。

- **HTTP設定**：
  - `port`: HTTPベースのストリーミング（HLS）用のポート。
  - `mediaroot`: ライブストリーミングファイルが保存されるディレクトリ。
  - `allow_origin`: どのドメインからのアクセスも許可するために '*' に設定。

- **トランスコーディング設定**：
  - トランスコーディングにはFFmpegを使用し、ビデオエンコーディングにはNVIDIA NVENCを使用。
  - オーディオは再エンコードせずに直接コピー。

### HLSストリーミングの詳細

- `hls_time`: 各HLSセグメントの時間（秒）。
- `hls_list_size`: プレイリスト内のセグメント数。
- `hls_flags`: ストレージ管理のためのセグメント削除を含む、HLSの挙動を制御するフラグ。

## サーバーの起動方法

サーバーを起動するには、以下を実行します：

```bash
node index.js
```