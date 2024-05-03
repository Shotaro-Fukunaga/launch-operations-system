import React from "react";
import LinearProgress from "@mui/material/LinearProgress";
import { TankStatus } from "../../../../types/rocketStatusType";
import StatusLabel from "./StatusLabel";

type Props = {
  title: string;
  tankStatus: TankStatus | undefined;
};

export const FuelTankStatus: React.FC<Props> = ({ title, tankStatus }) => {
  const liquidFuelAmount = tankStatus?.fuel?.amount ?? 0;
  const liquidFuelCapacity = tankStatus?.fuel?.max ?? 0;
  const oxidizerAmount = tankStatus?.lqd_oxygen?.amount ?? 0;
  const oxidizerCapacity = tankStatus?.lqd_oxygen?.max ?? 0;

  const liquidFuelPercentage =
    liquidFuelCapacity > 0 ? (liquidFuelAmount / liquidFuelCapacity) * 100 : 0;
  const oxidizerPercentage =
    oxidizerCapacity > 0 ? (oxidizerAmount / oxidizerCapacity) * 100 : 0;

  return (
    <div className="w-full h-full text-[0.6rem]">
      <div className="bg-gray-600  w-full flex justify-center">
        <h2 className="font-bold">{title}</h2>
      </div>

      <div className="p-[0.4rem] space-y-[0.1rem]">
        <div className="flex justify-between items-center w-full px-[1rem] font-medium">
          <h2>{tankStatus?.fuel?.name ?? ""}</h2>
          <h2>{liquidFuelPercentage.toFixed(2)}%</h2>
        </div>
        <LinearProgress variant="determinate" value={liquidFuelPercentage} />
        <p className="text-right">
          {liquidFuelAmount}/{liquidFuelCapacity}t
        </p>

        <div className="flex justify-between items-center w-full px-[0.4rem] font-medium">
          <h2>{tankStatus?.lqd_oxygen?.name ?? ""}</h2>
          <h2>{oxidizerPercentage.toFixed(2)}%</h2>
        </div>

        <LinearProgress variant="determinate" value={oxidizerPercentage} />
        <p className="text-right">
          {oxidizerAmount}/{oxidizerCapacity}t
        </p>
        <p>Temp : {tankStatus?.temperature ?? 0}</p>
        <p>Max Temp : {tankStatus?.max_temperature ?? 0}</p>
        <StatusLabel status={tankStatus?.status} />
      </div>
    </div>
  );
};
