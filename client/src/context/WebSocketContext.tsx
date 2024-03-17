import React, { createContext, useState, useEffect, ReactNode } from 'react'

export type WebSocketContextType = {
  sendMessage: (message: string) => void
  message: string
}
type WebSocketProviderProps = {
  children: ReactNode
}

export const WebSocketContext = createContext<WebSocketContextType | null>(null)

// export const useWebSocket = (): WebSocketContextType => {
//   const context = useContext(WebSocketContext)
//   if (context === null) {
//     throw new Error('useWebSocket must be used within a WebSocketProvider')
//   }
//   return context
// }



export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
}) => {
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [message, setMessage] = useState<string>('')

  useEffect(() => {
    if (!ws) {
      const websocket = new WebSocket('ws://localhost:8000/ws')

      websocket.onopen = () => {
        console.log('WebSocket Connected')
        setWs(websocket) // 接続が開かれたら、wsステートを更新
      }

      websocket.onmessage = (evt) => {
        const message = JSON.parse(evt.data)
        setMessage(message)
      }

      websocket.onclose = () => {
        console.log('WebSocket Disconnected')
        setWs(null) // 接続が閉じられたら、wsステートをnullにリセット
      }
    }

    // コンポーネントのアンマウント時にWebSocketを閉じない
    // return () => { websocket.close(); };
  }, [ws])

  const sendMessage = (message: string) => {
    if (ws) {
      ws.send(message)
    }
  }

  const value = {
    sendMessage,
    message,
  }

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  )
}
