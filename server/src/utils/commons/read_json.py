import json
from pathlib import Path


def read_json(file_path: str) -> dict:
    """JSONファイルを読み込む

    Args:
        file_path (str): JSONファイルのパス

    Returns:
        dict: JSONファイルの内容を辞書として返す
    """
    with Path(file_path).open() as file:
        return json.load(file)
