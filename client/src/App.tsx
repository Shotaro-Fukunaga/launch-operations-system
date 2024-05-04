// import { WebSocketProvider } from './context/WebSocketContext'
import { AppRoutes } from './routes/AppRoutes'
import 'chartjs-adapter-date-fns';

function App() {
  return (
    <>
      {/* <WebSocketProvider> */}
        <AppRoutes />
      {/* </WebSocketProvider> */}
    </>
  )
}

export default App
