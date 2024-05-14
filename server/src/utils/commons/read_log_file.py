"""ログファイルを読み込んでjsonのリストを返すモジュール"""

import json
import logging

import aiofiles

logger = logging.getLogger(__name__)


async def read_log_file(log_file_path: str) -> list:
    """ログファイルを読み込み、JSONオブジェクトのリストとして返す関数

    Args:
        log_file_path (str): 読み込むログファイルのパス

    Returns:
        list: JSONオブジェクトのリスト。ファイルが見つからない場合は空のリストを返す
    """
    logs = []
    try:
        async with aiofiles.open(log_file_path, "r") as file:
            return [json.loads(line) async for line in file]
    except FileNotFoundError:
        logger.exception("Log file not found")
    return logs
