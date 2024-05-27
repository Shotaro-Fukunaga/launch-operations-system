import { useEffect } from "react";
import * as Cesium from "cesium";
import { FlightRecord } from "../../types/flightRecordType";
import { CesiumComponentRef } from "resium";

/**
 * カメラの位置をスムーズに調整するための関数。
 * @param viewer Cesium.Viewer インスタンス。
 * @param start 開始位置。
 * @param end 終了位置。
 * @param startTime 開始時間（ミリ秒）。
 * @param endTime 終了時間（ミリ秒）。
 */
const adjustCamera = (
  viewer: Cesium.Viewer,
  start: Cesium.Cartesian3,
  end: Cesium.Cartesian3,
  startTime: number,
  endTime: number
) => {
  const easeInOutQuad = (t: number) =>
    t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
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

/**
 * フライトレコードを基にポジションを更新し、カメラを調整するカスタムフック。
 * @param viewerRef ReactのRefオブジェクト（Cesium.Viewer）。
 * @param positionsRef ポジションのRefオブジェクト。
 * @param previousPositionRef 以前のポジションのRefオブジェクト。
 * @param previousTimestampRef 以前のタイムスタンプのRefオブジェクト。
 * @param flightRecords フライトレコードの配列。
 */
export const useCesium = (
  viewerRef: React.MutableRefObject<CesiumComponentRef<Cesium.Viewer> | null>,
  positionsRef: React.MutableRefObject<Cesium.Cartesian3[]>,
  previousPositionRef: React.MutableRefObject<Cesium.Cartesian3 | null>,
  previousTimestampRef: React.MutableRefObject<number | null>,
  flightRecords: FlightRecord[]
) => {
  useEffect(() => {
    Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ACCESS_TOKEN;
  }, []);

  useEffect(() => {
    const viewer = viewerRef.current?.cesiumElement;

    if (viewer) {
      const polylineEntity = viewer.entities.add({
        name: "Rocket Trajectory",
        polyline: {
          positions: new Cesium.CallbackProperty(
            () => positionsRef.current,
            false
          ),
          width: 4,
          material: new Cesium.PolylineGlowMaterialProperty({
            glowPower: 0.2,
          }),
          arcType: Cesium.ArcType.GEODESIC,
        },
      });

      const updatePositions = () => {
        positionsRef.current = flightRecords.map((record) =>
          Cesium.Cartesian3.fromDegrees(
            record.longitude,
            record.latitude,
            record.altitude
          )
        );

        const latestRecord = flightRecords[flightRecords.length - 1];
        if (latestRecord) {
          const { latitude, longitude, altitude } = latestRecord;
          const end = Cesium.Cartesian3.fromDegrees(
            longitude + 1.1,
            latitude - 1.5,
            altitude
          );
          const offset = new Cesium.Cartesian3(0.0, 0.0, 110000.0);
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

      updatePositions();

      return () => {
        viewer.entities.remove(polylineEntity);
      };
    }
  }, [
    flightRecords,
    viewerRef,
    positionsRef,
    previousPositionRef,
    previousTimestampRef,
  ]);
};
