import React, { useEffect, useRef } from "react";
import { Viewer, Entity, CesiumComponentRef } from "resium";
import * as Cesium from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";

type FlightRecord = {
  latitude: number;
  longitude: number;
  altitude: number;
  // event?: string;
  display_log?: string;
};

type Props = {
  flightRecords: FlightRecord[];
};

const easeInOutQuad = (t: number) =>
  t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

const CesiumComponent: React.FC<Props> = ({ flightRecords }) => {
  const viewerRef = useRef<CesiumComponentRef<Cesium.Viewer>>(null);
  const positionsRef = useRef<Cesium.Cartesian3[]>([]);
  const previousPositionRef = useRef<Cesium.Cartesian3 | null>(null);
  const previousTimestampRef = useRef<number | null>(null);

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

      // カメラの位置と視点を調整
      const adjustCamera = (
        viewer: Cesium.Viewer,
        start: Cesium.Cartesian3,
        end: Cesium.Cartesian3,
        startTime: number,
        endTime: number
      ) => {
        const duration = endTime - startTime;

        const animate = (currentTime: number) => {
          const t = (currentTime - startTime) / duration;
          const easedT = easeInOutQuad(t);
          if (t > 1) {
            viewer.camera.setView({
              destination: end,
              orientation: {
                heading: Cesium.Math.toRadians(303.5222252867439),
                pitch: Cesium.Math.toRadians(-24.88213661971884),
                roll: Cesium.Math.toRadians(359.6511492310916 - 360),
              },
            });
            previousPositionRef.current = end;
            previousTimestampRef.current = endTime;
          } else {
            const interpolatedPosition = Cesium.Cartesian3.lerp(
              start,
              end,
              easedT,
              new Cesium.Cartesian3()
            );
            viewer.camera.setView({
              destination: interpolatedPosition,
              orientation: {
                heading: Cesium.Math.toRadians(303.5222252867439),
                pitch: Cesium.Math.toRadians(-24.88213661971884),
                roll: Cesium.Math.toRadians(359.6511492310916 - 360),
              },
            });
            requestAnimationFrame(animate);
          }
        };

        requestAnimationFrame(animate);
      };

      // 新しいフライトレコードが追加されたときにポジションを更新
      const updatePositions = (newRecords: FlightRecord[]) => {
        positionsRef.current = newRecords.map((record) =>
          Cesium.Cartesian3.fromDegrees(
            record.longitude,
            record.latitude,
            record.altitude
          )
        );

        // 最新のレコードを取得
        const latestRecord = newRecords[newRecords.length - 1];
        if (latestRecord) {
          const { latitude, longitude, altitude } = latestRecord;
          const end = Cesium.Cartesian3.fromDegrees(
            longitude + 1.1,
            latitude - 1.5,
            altitude
          );
          const offset = new Cesium.Cartesian3(0.0, 0.0, 110000.0); // 高度を保つオフセット
          const endPosition = Cesium.Cartesian3.add(
            end,
            offset,
            new Cesium.Cartesian3()
          );

          const now = performance.now();
          if (previousPositionRef.current && previousTimestampRef.current) {
            adjustCamera(
              viewer,
              previousPositionRef.current,
              endPosition,
              previousTimestampRef.current,
              now + 1000
            );
          } else {
            viewer.camera.setView({
              destination: endPosition,
              orientation: {
                heading: Cesium.Math.toRadians(303.5222252867439),
                pitch: Cesium.Math.toRadians(-24.88213661971884),
                roll: Cesium.Math.toRadians(359.6511492310916 - 360),
              },
            });
            previousPositionRef.current = endPosition;
            previousTimestampRef.current = now;
          }
        }
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
        animation={false} // アニメーションウィジェットを非表示に
        timeline={false} // タイムラインを非表示に
        baseLayerPicker={false} // 基本レイヤピッカーも非表示にする場合
        fullscreenButton={false} // フルスクリーンボタンを非表示に
        homeButton={false} // ホームボタンを非表示に
        geocoder={false} // ジオコーダを非表示（地理検索）
      >
        {flightRecords
          .filter((record) => record.display_log)
          .map((record, index) => (
            <React.Fragment key={index}>
              <Entity
                position={Cesium.Cartesian3.fromDegrees(
                  record.longitude,
                  record.latitude,
                  record.altitude
                )}
                // point={{ pixelSize: 10, color: Cesium.Color.WHITE }}
              />
              {record.display_log && ( // ここを変更
                <Entity
                  position={Cesium.Cartesian3.fromDegrees(
                    record.longitude,
                    record.latitude,
                    record.altitude
                  )}
                  label={{
                    text: record.display_log, // ここを変更
                    font: "14pt sans-serif",
                    style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                    outlineWidth: 2,
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                    pixelOffset: new Cesium.Cartesian2(0, -9),
                    distanceDisplayCondition:
                      new Cesium.DistanceDisplayCondition(0, 5000000), // 距離条件を設定して、表示距離を固定
                  }}
                />
              )}
            </React.Fragment>
          ))}
      </Viewer>
    </div>
  );
};

export default CesiumComponent;
