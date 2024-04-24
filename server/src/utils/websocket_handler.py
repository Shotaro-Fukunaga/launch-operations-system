import logging
import asyncio
from fastapi import WebSocket, WebSocket, WebSocketDisconnect


async def common_websocket_handler(websocket: WebSocket, data_function):
    """WebSocketを介してクライアントに定期的にデータを送信するための非同期ハンドラ

    Parameters:
        websocket (WebSocket): FastAPIのWebSocket接続オブジェクト。クライアントとの通信に使用する
        data_function (callable): データを生成する関数

    Raises:
        WebSocketDisconnect: WebSocket接続がクライアントによって閉じられた場合
        asyncio.CancelledError: WebSocketタスクがキャンセルされた場合
        Exception: データ送信中に予期しないエラーが発生した場合

    """
    await websocket.accept()
    try:
        while True:
            data = await asyncio.get_event_loop().run_in_executor(None, data_function)
            await websocket.send_json(data)
            await asyncio.sleep(1)  # 更新頻度を調整
    except WebSocketDisconnect:
        logging.info("WebSocket connection has been closed by the client.")
    except asyncio.CancelledError:
        logging.info("WebSocket task was cancelled")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        await websocket.close(code=1011, reason="Unexpected error occurred")