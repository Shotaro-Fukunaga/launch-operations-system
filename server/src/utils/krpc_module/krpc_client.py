import krpc
import time
import logging

class KrpcClient:
    def __init__(self, connection_name):
        self.connection_name = connection_name
        self.client = None
        self.is_initialized = False
        self.is_connected = False  # 接続状態を追跡
        self.max_retries = 24  # 24回リトライする
        self.retry_interval = 3  # seconds
        self.initialize(connection_name)

    def initialize(self, connection_name):
        retries = 0
        while retries < self.max_retries:
            try:
                self.client = krpc.connect(name=connection_name)
                self.is_initialized = True
                self.is_connected = True  # 接続成功を記録
                logging.info("KRPC connected successfully.")
                break  # 初期化に成功した場合はループを抜ける
            except Exception as e:
                self.is_connected = False  # 接続失敗を記録
                logging.error(f"Initialization failed, retrying in {self.retry_interval} seconds: {e}")
                time.sleep(self.retry_interval)
                retries += 1

        if retries == self.max_retries:
            logging.error("Failed to initialize Core after maximum retries.")
            raise Exception("Failed to initialize Core after maximum retries.")

    @property
    def connection_status(self):
        """接続状態を返すプロパティ"""
        return self.is_connected

    def disconnect(self):
        """接続を閉じるメソッド"""
        if self.client:
            self.client.close()
            self.is_connected = False
            logging.info("KRPC connection closed successfully.")
