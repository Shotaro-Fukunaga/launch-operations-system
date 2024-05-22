import { FC, useState } from "react";
import { OrbitInfoType } from "../../../../types/vesselTelemetryType";
import LaunchHeader from "./LaunchHeader";
import LaunchTimer from "./LaunchTimer";
import OrbitInfo from "./OrbitInfo";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import LaunchCommandModal, { CommandType } from "./LaunchCommandModal";
import RocketIcon from "@mui/icons-material/Rocket";

type Props = {
  orbitInfo?: OrbitInfoType;
  launchRelativeTime?: number;
  sendCommand: (command: object) => void;
};

// 種子島宇宙センターの位置情報
const tanegashimaLocation = {
  name: "種子島宇宙センター",
  latitude: 31.2510,
  longitude: 130.9180,
};

const LaunchScreen: FC<Props> = ({
  orbitInfo,
  launchRelativeTime,
  sendCommand,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [targetOrbit, setTargetOrbit] = useState({
    periapsis: 0,
    apoapsis: 0,
    inclination: 0,
    speed: 0,
  });
  const [launchTime, setLaunchTime] = useState<Date | null>(null);

  const handleLaunchClick = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  const handleModalSubmit = (command: CommandType) => {
    sendCommand(command);
    setTargetOrbit(command.target_orbit);
    setLaunchTime(command.launch_date);
  };

  return (
    <div className="w-full h-full">
      <LaunchHeader />
      <LaunchTimer
        launchTime={launchTime}
        launchRelativeTime={launchRelativeTime}
      />
      <OrbitInfo orbitInfo={orbitInfo} targetOrbit={targetOrbit} />
      <div className="flex justify-center w-full p-5">
        <button
          onClick={handleLaunchClick}
          className="flex items-center justify-center gap-2 text-white bg-gray-500"
        >
          <RocketIcon />
          Launch Sequence Settings
        </button>
      </div>
      <LaunchCommandModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        onSubmit={handleModalSubmit}
      />

    </div>
  );
};

export default LaunchScreen;
