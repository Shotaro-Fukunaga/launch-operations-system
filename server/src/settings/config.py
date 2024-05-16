from datetime import datetime, timedelta, timezone

from src.utils.commons.read_json import read_json

# KSPロケットの構造を設定したスキーマJSONファイルのパス
ROCKET_SCHEMAS = read_json("src/settings/rocket_schema.json").get("rocket_schemas", [])

# パーツのステータスコードの定義
WAIT = 0  # 待機中
GO = 1  # 準備完了
ACTIVE = 2  # 動作中
CUTOFF = 3  # カットオフ


# ログファイルのパス
FLIGHT_LOG_FILE_PATH = f"./src/logs/{datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d')}-los-flight.log"
