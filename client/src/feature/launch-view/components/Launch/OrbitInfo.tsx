import { FC } from "react";
import { OrbitInfoType } from "../../../../types/vesselTelemetryType";

type Props = {
  orbitInfo?: OrbitInfoType;
};

const OrbitInfo: FC<Props> = ({ orbitInfo }) => {
  return (
    <div className="w-full flex text-[0.8rem] pl-[0.8rem]">
      <div className="w-[50%] flex flex-col">
        <h3>Current Orbit</h3>
        <p>遠点高度: {orbitInfo?.apoapsis_altitude} m</p>
        <p>近点高度: {orbitInfo?.periapsis_altitude} m</p>
        <p>軌道速度: {orbitInfo?.orbital_speed} m/s</p>
        <p>軌道傾斜角: {orbitInfo?.inclination}°</p>
      </div>
      <div className="w-[50%] flex flex-col">
        <h3>Target Orbit</h3>
        <p>目標遠点高度: 200000 m</p>
        <p>目標近点高度: 200000 m</p>
        <p>目標軌道速度: 7788 m/s</p>
        <p>目標軌道傾斜角: 39.39°</p>
      </div>
    </div>
  );
};

export default OrbitInfo;
