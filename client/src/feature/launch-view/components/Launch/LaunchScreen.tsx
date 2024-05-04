import { FC } from "react";
import { OrbitInfoType } from "../../../../types/vesselTelemetryType";
import LaunchHeader from "./LaunchHeader";
import LaunchTimer from "./LaunchTimer";
import OrbitInfo from "./OrbitInfo";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";

type Props = {
  orbitInfo?: OrbitInfoType;
  launchRelativeTime?: string
  sendCommand: (command: object) => void;
};

const LaunchScreen: FC<Props> = ({ orbitInfo,launchRelativeTime,sendCommand }) => {
  const launchTime = new Date();
  launchTime.setMinutes(launchTime.getMinutes() + 1);
  const handleLaunchClick = () => {
    const command = {
      launch_date: launchTime,
      command: "sequence",
      target_orbit: {
        periapsis: 200000,
        apoapsis: 200000,
        inclination: 39.39,
        speed: 7788
      }
    };
    sendCommand(command);
  };
  return (
    <div className="w-full h-full">
      <LaunchHeader />
      <LaunchTimer launchTime={launchTime} launchRelativeTime={launchRelativeTime}/>
      <OrbitInfo orbitInfo={orbitInfo} />
      <div className="flex justify-center w-full p-5">
        <button onClick={handleLaunchClick} className="flex items-center justify-center gap-2 text-white bg-blue-500">
          <RocketLaunchIcon />
          Launch sequence start
        </button>
      </div>
    </div>
  );
};

export default LaunchScreen;
