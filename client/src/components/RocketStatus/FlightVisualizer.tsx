import RocketComponent from "./RocketSvg";
import { RocketEngineStatus } from "./EngineStatus";
import { FuelTankStatus } from "./FuelTankStatus";
import { FairingStatus } from "./FairingStatus";
import SatelliteBusStatus from "./SatelliteBusStatus";
import { RocketStatusType } from "../../types/rocketStatusType";

type Props = {
  rocketStatus?: RocketStatusType;
};

export const FlightVisualizer: React.FC<Props> = ({ rocketStatus }) => {
  return (
    <>
      <div className="flex w-full h-full">
        <div className="h-full w-[35%] flex flex-col">
          <div className="h-[40%] w-full">
            <SatelliteBusStatus
              title="Satellite Bus"
              satelliteBusStatus={rocketStatus?.satellite_bus}
              solarPanelStatus1={rocketStatus?.solar_panel_1}
              solarPanelStatus2={rocketStatus?.solar_panel_2}
            />
          </div>

          <div className="h-[30%] w-full">
            <FuelTankStatus
              title={"Second Tank"}
              tankStatus={rocketStatus?.second_tank}
            />
          </div>

          <div className="h-[30%] w-full">
            <FuelTankStatus
              title={"Main Tank"}
              tankStatus={rocketStatus?.main_tank}
            />
          </div>
        </div>

        <div className="h-full w-[30%] flex-col content-end border-l border-r border-gray-500">
          <RocketComponent
            fairingStatus={rocketStatus?.fairing_1?.status ?? 0}
            secondStageStatus={rocketStatus?.second_engine?.status ?? 0}
            firstStageStatus={rocketStatus?.main_engine?.status ?? 0}
          />
        </div>

        <div className="h-full w-[35%] flex flex-col">
          <div className="h-[20%] w-full">
            <FairingStatus
              title={"Fairing"}
              fairing1={rocketStatus?.fairing_1}
              fairing2={rocketStatus?.fairing_2}
            />
          </div>

          <div className="h-[40%] w-full">
            <RocketEngineStatus
              title="Second Engine Status"
              engineStatus={rocketStatus?.second_engine}
            />
          </div>

          <div className="h-[40%] w-full">
            <RocketEngineStatus
              title="Main Engine Status"
              engineStatus={rocketStatus?.main_engine}
            />
          </div>
        </div>
      </div>
    </>
  );
};
