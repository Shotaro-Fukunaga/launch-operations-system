import krpc
import logging
import threading
import time
from krpc.error import RPCError, ConnectionError


class KrpcClient:
    def __init__(self, connection_name, check_interval=5):
        self.connection_name = connection_name
        self.client = None
        self.is_connected = False  # 接続状態を追跡
        self.check_interval = check_interval  # 接続状態のチェック間隔（秒）
        self.initialize(connection_name)
        self.monitor_thread = threading.Thread(target=self.monitor_connection, daemon=True)
        self.monitor_thread.start()

    def initialize(self, connection_name):
        self.close_existing_client()  # 既存のクライアントを閉じる
        try:
            self.client = krpc.connect(name=connection_name)
            self.is_connected = True  # 接続成功を記録
            logging.info("KRPC connected successfully.")
        except Exception as e:
            self.is_connected = False  # 接続失敗を記録
            logging.error(f"Initialization failed: {e}")
            raise Exception("Failed to initialize Core.") from e

    @property
    def connection_status(self):
        """接続状態を返すプロパティ"""
        return self.is_connected

    def reconnect(self):
        """再接続を試みるメソッド"""
        logging.info("Attempting to reconnect to KRPC...")
        self.initialize(self.connection_name)

    def close_existing_client(self):
        """既存のクライアントを閉じるメソッド"""
        if self.client is not None:
            try:
                self.client.close()
                logging.info("Existing KRPC client closed.")
            except Exception as e:
                logging.warning(f"Failed to close existing client: {e}")
            finally:
                self.client = None

    def disconnect(self):
        """接続を閉じるメソッド"""
        if self.client:
            self.client.close()
            self.is_connected = False
            logging.info("KRPC connection closed successfully.")

    def monitor_connection(self):
        """接続状態を定期的にチェックするメソッド"""
        while True:
            try:
                # 接続状態をチェックする簡単なRPCを実行
                if self.is_connected:
                    self.client.space_center.active_vessel
                else:
                    self.reconnect()
            except (RPCError, ConnectionError) as e:
                logging.warning(f"Connection lost: {e}. Attempting to reconnect...")
                self.is_connected = False
                self.reconnect()
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
            time.sleep(self.check_interval)

    def execute_with_reconnect(self, function, *args, **kwargs):
        """
        指定された関数を再接続を試みながら実行する
        :param function: 実行する関数
        :param args: 関数に渡す引数
        :param kwargs: 関数に渡すキーワード引数
        :return: 関数の戻り値
        """
        try:
            if not self.is_connected:
                self.reconnect()

            # ゲームシーンをチェック
            scene = self.client.krpc.current_game_scene
            if scene == "flight":
                return function(*args, **kwargs)
            else:
                logging.warning(f"Function {function.__name__} not executed: Invalid game scene '{scene}'.")
                return None
        except RPCError as e:
            logging.error(f"RPCError occurred: {e}, attempting to reconnect...")
            self.reconnect()
            return function(*args, **kwargs)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
