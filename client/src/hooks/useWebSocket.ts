import { useContext } from 'react'
import {
  WebSocketContext,
  WebSocketContextType,
} from '../context/WebSocketContext'

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext)
  if (context === null) {
    throw new Error('useWebSocket must be used within a WebSocketProvider')
  }
  return context
}
