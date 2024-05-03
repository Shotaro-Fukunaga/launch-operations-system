import React, { useEffect, useRef } from "react";
import { Viewer, Entity, CesiumComponentRef } from "resium";
import * as Cesium from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";

type FlightRecord = {
  latitude: number;
  longitude: number;
  altitude: number;
};

type Props = {
  flightRecords: FlightRecord[];
};

const CesiumComponent: React.FC<Props> = ({ flightRecords }) => {
  const viewerRef = useRef<CesiumComponentRef<Cesium.Viewer>>(null);

  useEffect(() => {
    Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ACCESS_TOKEN;
  }, []);

  useEffect(() => {
    const viewer = viewerRef.current?.cesiumElement;
    if (viewer && flightRecords.length > 0) {
      const positions = flightRecords.map((record) =>
        Cesium.Cartesian3.fromDegrees(
          record.longitude,
          record.latitude,
          record.altitude
        )
      );

      const entity = viewer.entities.add({
        name: "Rocket Trajectory",
        polyline: {
          positions: positions,
          width: 5,
          material: Cesium.Color.RED,
        },
      });

      viewer.zoomTo(entity);
    }

    return () => {
      if (viewer) {
        viewer.entities.removeAll();
      }
    };
  }, [flightRecords]);

  return (
    <div className="h-full w-full">
      <Viewer
        ref={viewerRef}
        style={{ height: "100%", width: "100%" }}
        animation={false}  // アニメーションウィジェットを非表示に
        timeline={false}   // タイムラインを非表示に
        baseLayerPicker={false} // 基本レイヤピッカーも非表示にする場合
        fullscreenButton={false}     // フルスクリーンボタンを非表示に
        homeButton={false}           // ホームボタンを非表示に
        geocoder={false}             // ジオコーダを非表示（地理検索）
        
      >
        {flightRecords.map((record, index) => (
          <Entity
            key={index}
            position={Cesium.Cartesian3.fromDegrees(
              record.longitude,
              record.latitude,
              record.altitude
            )}
            point={{ pixelSize: 10, color: Cesium.Color.WHITE }}
          />
        ))}
      </Viewer>
    </div>
  );
};

export default CesiumComponent;
