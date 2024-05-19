import json
import logging
from pathlib import Path
from typing import Any

import aiofiles

logger = logging.getLogger(__name__)


class LogManager:
    """ログファイルを管理するクラス"""

    @staticmethod
    def save_to_log_sync(data: dict[str, Any], log_file_path: Path) -> None:
        """同期版: ログファイルにデータを保存する"""
        with log_file_path.open("a") as f:
            f.write(json.dumps(data) + "\n")

    @staticmethod
    async def save_to_log_async(data: dict[str, Any], log_file_path: Path) -> None:
        """非同期版: ログファイルにデータを保存する"""
        async with aiofiles.open(log_file_path, "a") as f:
            await f.write(json.dumps(data) + "\n")

    @staticmethod
    def read_log_file_sync(log_file_path: Path) -> list[dict[str, Any]]:
        """同期版: ログファイルを読み込み、JSONオブジェクトのリストとして返す関数"""
        try:
            with log_file_path.open("r") as file:
                return [json.loads(line) for line in file]
        except FileNotFoundError:
            logger.exception("Log file not found")
            return []

    @staticmethod
    async def read_log_file_async(log_file_path: Path) -> list[dict[str, Any]]:
        """非同期版: ログファイルを読み込み、JSONオブジェクトのリストとして返す関数"""
        try:
            async with aiofiles.open(log_file_path, "r") as file:
                return [json.loads(line) async for line in file]
        except FileNotFoundError:
            logger.exception("Log file not found")
            return []

    @staticmethod
    async def read_log_file_with_key_async(log_file_path: Path, key: str) -> list[dict[str, Any]]:
        """特定のキーが存在するレコードのみを非同期で取得する関数"""
        logs = []
        try:
            async with aiofiles.open(log_file_path, "r") as file:
                async for line in file:
                    line = line.strip()
                    if not line:  # 空行をスキップ
                        continue
                    try:
                        record = json.loads(line)
                        if key in record:
                            logs.append(record)
                    except json.JSONDecodeError:
                        logger.warning(f"Skipping invalid JSON line: {line}")
        except FileNotFoundError:
            logger.exception("Log file not found")
        return logs

    @staticmethod
    def truncate_to_seconds(iso_timestamp: str) -> str:
        """ISO 8601タイムスタンプを秒単位までにトリミングする"""
        return iso_timestamp[:19]

    @staticmethod
    def update_log_record_sync(log_file_path: Path, key: str, target_value: str | int, new_data: dict[str, Any]) -> None:
        """同期版: 特定の時間のログレコードを更新する関数"""
        logs = []
        new_record = None

        try:
            with log_file_path.open("r") as file:
                for line in file:
                    record: dict = json.loads(line)
                    if record.get(key) == target_value:
                        new_record = record.copy()
                        new_record.update(new_data)
                    logs.append(record)
                if new_record:
                    logs.append(new_record)
        except FileNotFoundError:
            logger.exception("Log file not found")
            return

        try:
            with log_file_path.open("w") as file:
                for record in logs:
                    file.write(json.dumps(record) + "\n")
        except Exception:
            logger.exception("Failed to write to log file")

    @staticmethod
    async def update_log_record_async(log_file_path: Path, key: str, target_value: str | int, new_data: dict[str, Any]) -> None:
        """非同期版: 特定のキーと値に基づいてログレコードを更新する関数

        Args:
            log_file_path (Path): ログファイルのパス
            key (str): 更新したいレコードのキー
            target_value (Any): 更新したいレコードのキーの値
            new_data (Dict[str, Any]): 更新するデータの辞書
        """
        logs = []
        new_record = None

        try:
            async with aiofiles.open(log_file_path, "r") as file:
                async for line in file:
                    record: dict = json.loads(line)
                    if record.get(key) == target_value:
                        new_record = record.copy()
                        new_record.update(new_data)
                    logs.append(record)
                if new_record:
                    logs.append(new_record)
        except FileNotFoundError:
            logger.exception("Log file not found")
            return

        try:
            async with aiofiles.open(log_file_path, "w") as file:
                for record in logs:
                    await file.write(json.dumps(record) + "\n")
        except Exception:
            logger.exception("Failed to write to log file")
