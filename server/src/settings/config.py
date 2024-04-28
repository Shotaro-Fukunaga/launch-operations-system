


import json


file_path = 'src/rocket_schema.json'

# JSONファイルを開いて読み込む
with open(file_path, 'r') as file:
    rocket_data = json.load(file)


ROCKET_SCHEMAS = rocket_data['rocket_schemas']