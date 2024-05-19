import logging
import threading
import time
from typing import Any, Callable

import krpc
from krpc.error import ConnectionError, RPCError

logger = logging.getLogger(__name__)


class KrpcClient:
    """KRPCクライアントを管理するクラス"""

    def __init__(self: "KrpcClient", connection_name: str, check_interval: int = 5) -> None:
        """Initialize the KrpcClient class."""
        self.connection_name = connection_name
        self.client = None
        self.is_connected = False  # 接続状態を追跡
        self.check_interval = check_interval  # 接続状態のチェック間隔（秒）
        self.initialize(connection_name)
        self.monitor_thread = threading.Thread(target=self.monitor_connection, daemon=True)
        self.monitor_thread.start()

    def initialize(self: "KrpcClient", connection_name: str) -> None:
        """KRPCクライアントを初期化するメソッド"""
        self.close_existing_client()  # 既存のクライアントを閉じる
        try:
            self.client = krpc.connect(name=connection_name)
            self.is_connected = True  # 接続成功を記録
            logger.info("KRPC connected successfully.")
        except Exception:
            self.is_connected = False  # 接続失敗を記録
            logger.exception("Initialization failed")
            raise

    @property
    def connection_status(self: "KrpcClient") -> bool:
        """接続状態を返すプロパティ"""
        return self.is_connected

    def reconnect(self: "KrpcClient") -> None:
        """再接続を試みるメソッド"""
        logger.info("Attempting to reconnect to KRPC...")
        self.initialize(self.connection_name)

    def close_existing_client(self: "KrpcClient") -> None:
        """既存のクライアントを閉じるメソッド"""
        if self.client is not None:
            try:
                self.client.close()
                logger.info("Existing KRPC client closed.")
            except (RPCError, ConnectionError) as e:
                logger.warning("Failed to close existing client %s", e)
            finally:
                self.client = None

    def disconnect(self: "KrpcClient") -> None:
        """接続を閉じるメソッド"""
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("KRPC connection closed successfully.")

    def monitor_connection(self: "KrpcClient") -> None:
        """接続状態を定期的にチェックするメソッド"""
        while True:
            try:
                # 接続状態をチェックする簡単なRPCを実行
                if self.is_connected:
                    if self.client and hasattr(self.client, "space_center") and self.client.space_center:
                        _ = self.client.space_center.active_vessel
                    else:
                        logger.warning("Space Center is not available.")
                        self.is_connected = False
                        self.reconnect()
                else:
                    self.reconnect()
            except (RPCError, ConnectionError) as e:
                logger.warning("Connection lost: %s. Attempting to reconnect...", e)
                self.is_connected = False
                self.reconnect()
            except Exception:
                logger.exception("Unexpected error")
            time.sleep(self.check_interval)

    def execute_with_reconnect(self: "KrpcClient", function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any | None:  # noqa: ANN401
        """接続が失われた場合に再接続を試みながら指定された関数を実行する

        Args:
            function (Callable[..., Any]): 実行する関数
            *args (Any): 関数に渡す位置引数
            **kwargs (Any): 関数に渡すキーワード引数

        Returns:
            Any | None: 実行された関数の戻り値。または、ゲームシーンが「flight」でない場合、
                        または関数が実行できなかった場合はNoneを返す
        """
        try:
            if not self.is_connected:
                self.reconnect()

            # ゲームシーンをチェック
            if self.client and hasattr(self.client, "krpc") and self.client.krpc:
                scene = self.client.krpc.current_game_scene
                if scene == "flight":
                    return function(*args, **kwargs)
                logger.warning("Function %s not executed: Invalid game scene '%s'.", function.__name__, scene)
            else:
                logger.warning("KRPC client is not available.")
            return None
        except RPCError:
            logger.exception("RPCError occurred: attempting to reconnect...")
            self.reconnect()
            return function(*args, **kwargs)
        except Exception:
            logger.exception("Unexpected error")
            raise
