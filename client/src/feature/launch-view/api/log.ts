import { Log } from '../types/log'

// WebSocketを通じてログデータを取得する関数
// WebSocketを通じてログデータを取得する関数
export const fetchLogs = (
  setLogs: React.Dispatch<React.SetStateAction<Log[]>>
): (() => void) => {
  const ws = new WebSocket('ws://localhost:8765')

  ws.onmessage = (event) => {
    const message: Log = JSON.parse(event.data);
    // 受信メッセージのタイムスタンプを別のプロパティに保存する場合
    // const receivedTimestamp = message.timestamp; // 仮定: 受信メッセージにtimestampがある
    const newTimestamp = new Date().toLocaleTimeString();
    // 受信したタイムスタンプを保持しつつ、新しいタイムスタンプも追加
    const log: Log = { ...message, timestamp: newTimestamp };
    setLogs((prevLogs) => [...prevLogs, log]);
  }

  // WebSocketをクローズするためのクリーンアップ関数を返します
  return () => {
    ws.close();
  }
}

