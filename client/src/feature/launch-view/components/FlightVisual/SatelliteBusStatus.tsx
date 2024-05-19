import React from "react";
import {
  SatelliteBusStatusType,
  SolarPanelStatus,
} from "../../../../types/rocketStatusType";
import SatelliteAltIcon from "@mui/icons-material/SatelliteAlt";
import StatusLabel from "./StatusLabel";
import SolarPowerIcon from "@mui/icons-material/SolarPower";
import SignalCellularAltIcon from "@mui/icons-material/SignalCellularAlt";

interface Props {
  title: string;
  satelliteBusStatus?: SatelliteBusStatusType;
  solarPanelStatus1?: SolarPanelStatus;
  solarPanelStatus2?: SolarPanelStatus;
}

const SatelliteBusStatus: React.FC<Props> = ({
  title,
  satelliteBusStatus,
  solarPanelStatus1,
  solarPanelStatus2,
}) => {
  return (
    <div className="w-full h-full text-[0.6rem]">
      <div className="text-center bg-gray-600">
        <h2 className="font-bold">{title}</h2>
      </div>

      <div className="flex flex-col gap-[0.4rem]">
        {/* Satellite Bus */}
        <div className="flex gap-[0.4rem]">
          <SatelliteAltIcon fontSize="small" />
          <div className="flex flex-col">
            <h3 className="font-semibold">Satellite Bus Status</h3>
            <StatusLabel status={satelliteBusStatus?.status} />
            <p>
              Charge: {satelliteBusStatus?.current_charge ?? 0} /{" "}
              {satelliteBusStatus?.max_charge ?? 0}
            </p>
          </div>
        </div>

        {/* Communication */}
        <div className="flex gap-[0.4rem]">
          <SignalCellularAltIcon fontSize="small" />
          <div className="flex flex-col">
            <h3 className="font-semibold">Communication Status</h3>
            <p>
              Communicate: {satelliteBusStatus?.can_communicate ? "Yes" : "No"}
            </p>
            <p>
              Transmit Science:{" "}
              {satelliteBusStatus?.can_transmit_science ? "Yes" : "No"}
            </p>
            <p>Signal Str: {satelliteBusStatus?.signal_strength ?? 0}</p>
            <p>Signal Delay: {satelliteBusStatus?.signal_delay ?? 0}</p>
            <p>Total Comm Power: {satelliteBusStatus?.total_comm_power ?? 0}</p>
          </div>
        </div>

        {/* Solar Panel */}
        <div className="flex gap-[0.4rem]">
          <SolarPowerIcon fontSize="small" />
          <div className="flex flex-col">
            <h3 className="font-semibold">Solar Panel Status #1 #2</h3>
            <StatusLabel status={solarPanelStatus1?.status} />
            <p>
              Energy Flow: {solarPanelStatus1?.energy_flow ?? 0} :{" "}
              {solarPanelStatus2?.energy_flow ?? 0}
            </p>
            <p>
              Sun Exposure: {solarPanelStatus1?.sun_exposure ?? 0} :{" "}
              {solarPanelStatus2?.sun_exposure ?? 0}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SatelliteBusStatus;
