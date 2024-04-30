import json

from src.utils.krpc_module.rocket_core import RocketCore


# JSONファイルを開いて読み込む
def open_json(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# TODO あとでリファクタリングする
EVENT_PLANS = open_json("src/event_records/event_record_plans.json")
FLIGHT_PLANS = open_json("src/flight_records/flight_record_plans.json")
ROCKET_SCHEMAS = open_json("src/rocket_schema.json")
rocket_schema_list = ROCKET_SCHEMAS.get("rocket_schemas", [])


base_rocket = RocketCore(connection="python_api", rocket_schema_list=rocket_schema_list)
