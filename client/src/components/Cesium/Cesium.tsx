import { FC, useEffect } from "react";
import * as Cesium from "cesium";
import { Viewer, Entity } from "resium";
import "cesium/Build/Cesium/Widgets/widgets.css";
import { FlightRecord } from "../../types/flightRecordType";

type Props = {
  flightRecords: FlightRecord[];
};

const CesiumComponent: FC<Props> = ({ flightRecords }) => {
  useEffect(() => {
    Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_ACCESS_TOKEN;
  }, []);

  const positions = flightRecords.map((data) =>
    Cesium.Cartesian3.fromDegrees(data.longitude, data.latitude, data.altitude)
  );

  return (
    <div className="h-full w-full">
      <Viewer style={{ height: "100%", width: "100%" }}>
        <Entity
          name="Rocket Trajectory"
          polyline={{
            positions: positions,
            width: 5,
            material: Cesium.Color.RED,
          }}
        />
      </Viewer>
    </div>
  );
};

export default CesiumComponent;
