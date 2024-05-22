import { FC } from "react";
import { OrbitInfoType } from "../../../../types/vesselTelemetryType";

type Props = {
  orbitInfo?: OrbitInfoType;
  targetOrbit: {
    periapsis: number;
    apoapsis: number;
    inclination: number;
    speed: number;
  };
};

const OrbitInfo: FC<Props> = ({ orbitInfo, targetOrbit }) => {
  return (
    <div className="w-full flex text-[0.8rem] pl-[0.8rem]">
      <div className="w-[50%] flex flex-col">
        <h3>Current Orbit</h3>
        <p>遠点高度: {orbitInfo?.apoapsis_altitude ?? 0} m</p>
        <p>近点高度: {orbitInfo?.periapsis_altitude ?? 0} m</p>
        <p>軌道速度: {orbitInfo?.orbital_speed ?? 0} m/s</p>
        <p>軌道傾斜角: {orbitInfo?.inclination ?? 0}°</p>
      </div>
      <div className="w-[50%] flex flex-col">
        <h3>Target Orbit</h3>
        <p>目標遠点高度: {targetOrbit.apoapsis ?? 0} m</p>
        <p>目標近点高度: {targetOrbit.periapsis ?? 0} m</p>
        <p>目標軌道速度: {targetOrbit.speed ?? 0} m/s</p>
        <p>目標軌道傾斜角: {targetOrbit.inclination ?? 0}°</p>
      </div>
    </div>
  );
};

export default OrbitInfo;
