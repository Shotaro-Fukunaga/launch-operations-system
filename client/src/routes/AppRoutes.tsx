import { Route, Routes } from 'react-router-dom'
import { LaunchDataViewer } from '../feature/launch-view/page/LaunchDataViewer'
import { OrbitView } from '../page/OrbitView'
import { RocketDetails } from '../page/RocketDetails'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<LaunchDataViewer />}></Route>
      <Route path="/orbital-view" element={<OrbitView />}></Route>
      <Route path="/rocket-details" element={<RocketDetails />}></Route>
    </Routes>
  )
}
