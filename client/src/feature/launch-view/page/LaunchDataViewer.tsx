import { BasicLayout } from '../../../components/Layout/BasicLayout'
import { TimelineBar } from '../components/VerticalTimeLine/TimelineBar'
import { FlightVisualizer } from '../components/FlightVisual/FlightVisualizer'
import { LivePlayer } from '../../../components/Live/LivePlayer'
import CesiumComponent from '../../../components/Cesium/Cesium'

export const LaunchDataViewer = () => {
  return (
    <BasicLayout>
      <div className="flex flex-wrap h-full">
        {/* 上段 */}
        <div className="flex h-[55%] w-full">
          {/* 機首の方向・機体の速度 */}
          <div className="border border-gray-500 w-[20%] h-full">
            <p>mean_altitude: 300000m ±1000</p>
            <p>periapsis_altitude: 300000m ±1000</p>
            <p>velocity: 300000m ±1000</p>
            heading roll pitch
          </div>

          {/* 軌道の表示 */}
          <div className="border border-gray-500 w-[60%] h-full">
            <CesiumComponent />
          </div>

          {/* 進行中のタスク */}
          <div className="w-[20%] h-full bg-[#242424]">
            <TimelineBar
              events={[
                { time: '13:00', name: 'LIFT OFF', color: 'green' },
                { time: '16:00', name: 'MECO', color: 'green' },
                { time: '16:18', name: 'HOGE', color: 'yellow' },
                { time: '21:18', name: 'HOGE', color: 'red' },
              ]}
            />
          </div>
        </div>

        {/* 下段 */}
        <div className="flex h-[45%] w-full">
          <div className="border border-gray-500 w-[60%] h-full flex bg-gray-200">
            <div className="w-[50%] border border-blue-600">
              <FlightVisualizer />
            </div>
            <div className="w-[50%] border border-pink-600">お天気の情報</div>
          </div>

          {/* OBSストリームを表示する */}
          <div className="w-[40%] h-full border border-gray-500 flex justify-center">
            <LivePlayer />
          </div>
        </div>
      </div>
    </BasicLayout>
  )
}
