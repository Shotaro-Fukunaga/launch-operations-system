import React, { useRef } from "react";
import { Viewer, Entity, CesiumComponentRef } from "resium";
import * as Cesium from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";
import { FlightRecord } from "../../types/flightRecordType";
import { useCesium } from "./useCesium";

type Props = {
  flightRecords: FlightRecord[];
};

/**
 * CesiumComponent
 * @param {Props} props - The component props.
 * @returns {JSX.Element} The rendered component.
 */
const CesiumComponent: React.FC<Props> = ({ flightRecords }) => {
  const viewerRef = useRef<CesiumComponentRef<Cesium.Viewer>>(null);
  const positionsRef = useRef<Cesium.Cartesian3[]>([]);
  const previousPositionRef = useRef<Cesium.Cartesian3 | null>(null);
  const previousTimestampRef = useRef<number | null>(null);

  useCesium(
    viewerRef,
    positionsRef,
    previousPositionRef,
    previousTimestampRef,
    flightRecords
  );

  return (
    <div className="w-full h-full">
      <Viewer
        ref={viewerRef}
        style={{ height: "100%", width: "100%" }}
        animation={false}
        timeline={false}
        baseLayerPicker={false}
        fullscreenButton={false}
        homeButton={false}
        geocoder={false}
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
              />
              {record.display_log && (
                <Entity
                  position={Cesium.Cartesian3.fromDegrees(
                    record.longitude,
                    record.latitude,
                    record.altitude
                  )}
                  label={{
                    text: record.display_log,
                    font: "14pt sans-serif",
                    style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                    outlineWidth: 2,
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                    pixelOffset: new Cesium.Cartesian2(0, -9),
                    distanceDisplayCondition:
                      new Cesium.DistanceDisplayCondition(0, 5000000),
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
