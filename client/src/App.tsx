import { WebSocketProvider } from './context/WebSocketContext'
import { AppRoutes } from './routes/AppRoutes'

function App() {
  return (
    <>
      <WebSocketProvider>
        <AppRoutes />
      </WebSocketProvider>
    </>
  )
}

export default App
