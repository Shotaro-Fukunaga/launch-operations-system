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
  const positionsRef = useRef<Cesium.Cartesian3[]>([]);
  
  useEffect(() => {
    Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ACCESS_TOKEN;
  }, []);


  useEffect(() => {
    const viewer = viewerRef.current?.cesiumElement;

    if (viewer) {
      // 初期のポリラインエンティティを作成
      const polylineEntity = viewer.entities.add({
        name: "Rocket Trajectory",
        polyline: {
          positions: new Cesium.CallbackProperty(() => {
            return positionsRef.current;
          }, false),
          width: 4,
          material: new Cesium.PolylineGlowMaterialProperty({
            glowPower: 0.2,
            // color: Cesium.Color.RED,
          }),
          arcType: Cesium.ArcType.GEODESIC,
        },
      });

      // 新しいフライトレコードが追加されたときにポジションを更新
      const updatePositions = (newRecords: FlightRecord[]) => {
        positionsRef.current = newRecords.map(record =>
          Cesium.Cartesian3.fromDegrees(
            record.longitude,
            record.latitude,
            record.altitude
          )
        );
      };

      // 初回ロード時にポジションを設定
      updatePositions(flightRecords);

      // フライトレコードが更新されるたびにポジションを更新
      return () => {
        viewer.entities.remove(polylineEntity);
      };
    }
  }, [flightRecords]);

  return (
    <div className="w-full h-full">
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
            // point={{ pixelSize: 10, color: Cesium.Color.WHITE }}
          />
        ))}
      </Viewer>
    </div>
  );
};

export default CesiumComponent;
