import { useCallback, useEffect, useRef, useState } from 'react'
import * as Cesium from 'cesium'
import { Cartesian3, ScreenSpaceEventHandler } from 'cesium'
import { Viewer, Entity, CameraFlyTo } from 'resium'
import 'cesium/Build/Cesium/Widgets/widgets.css'

const CesiumComponent = () => {
  useEffect(() => {
    Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ACCESS_TOKEN
  }, [])

  const destination = Cartesian3.fromDegrees(139.767052, 35.681167, 1000)

  const viewerRef = useRef<Cesium.Viewer | null>(null)

  const sensitivity = 2
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!viewerRef.current) return

      const camera = viewerRef.current.camera
      switch (event.key) {
        case 'ArrowUp':
          camera.setView({
            orientation: {
              heading: camera.heading,
              pitch: camera.pitch + Cesium.Math.toRadians(sensitivity),
              roll: camera.roll,
            },
          })
          break
        case 'ArrowDown':
          camera.setView({
            orientation: {
              heading: camera.heading,
              pitch: camera.pitch - Cesium.Math.toRadians(sensitivity),
              roll: camera.roll,
            },
          })
          break
        case 'ArrowLeft':
          camera.setView({
            orientation: {
              heading: camera.heading - Cesium.Math.toRadians(sensitivity),
              pitch: camera.pitch,
              roll: camera.roll,
            },
          })
          break
        case 'ArrowRight':
          camera.setView({
            orientation: {
              heading: camera.heading + Cesium.Math.toRadians(sensitivity),
              pitch: camera.pitch,
              roll: camera.roll,
            },
          })
          break
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  // const viewerRef = useRef<Cesium.Viewer | null>(null)

  // useEffect(() => {
  //   if (viewerRef.current) {
  //     const viewer = viewerRef.current.cesiumElement
  //     if (viewer) {
  //       viewer.scene.screenSpaceCameraController.zoomEventTypes = [
  //         Cesium.CameraEventType.WHEEL,
  //       ]

  //       const handler = new Cesium.ScreenSpaceEventHandler(viewer.canvas)

  //       handler.setInputAction(
  //         (movement: ScreenSpaceEventHandler.MotionEvent) => {
  //           const camera = viewer.camera
  //           const deltaX = movement.endPosition.x - movement.startPosition.x
  //           const deltaY = movement.endPosition.y - movement.startPosition.y

  //           const headingChange = deltaX * Cesium.Math.toRadians(0.1) // 感度調整
  //           const pitchChange = deltaY * Cesium.Math.toRadians(0.1) // 感度調整

  //           camera.setView({
  //             orientation: {
  //               heading: camera.heading - headingChange,
  //               pitch: camera.pitch - pitchChange,
  //               roll: camera.roll,
  //             },
  //           })
  //         },
  //         Cesium.ScreenSpaceEventType.MOUSE_MOVE
  //       )

  //       return () => {
  //         if (handler) {
  //           handler.destroy()
  //         }
  //       }
  //     }
  //   }
  // }, [viewerRef])

  return (
    <div className="h-full w-full">
      <Viewer style={{ height: '100%', width: '100%' }}>
        <Entity position={destination} point={{ pixelSize: 10 }} />
        <CameraFlyTo
          destination={destination}
          orientation={{
            heading: Cesium.Math.toRadians(10), // 左右の回転
            pitch: Cesium.Math.toRadians(-30), // 上下の角度
            roll: 0.0,
          }}
          // duration={2} // 移動にかかる時間（秒）
        />
      </Viewer>
    </div>
  )
}

export default CesiumComponent
