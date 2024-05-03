import { FC } from "react";
import { OrbitInfoType } from "../../../../types/vesselTelemetryType";
import LaunchHeader from "./LaunchHeader";
import LaunchTimer from "./LaunchTimer";
import OrbitInfo from "./OrbitInfo";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";

type Props = {
  orbitInfo?: OrbitInfoType;
};

const LaunchScreen: FC<Props> = ({ orbitInfo }) => {
  const launchTime = new Date();
  launchTime.setMinutes(launchTime.getMinutes() + 10);
  return (
    <div className="w-full h-full">
      <LaunchHeader />
      <LaunchTimer launchTime={launchTime} />
      <OrbitInfo orbitInfo={orbitInfo} />
      <div className="w-full flex justify-center p-5">
        <button className="bg-blue-500 text-white flex items-center justify-center gap-2">
          <RocketLaunchIcon />
          Launch sequence start
        </button>
      </div>
    </div>
  );
};

export default LaunchScreen;
