import React from "react";
import LinearProgress from "@mui/material/LinearProgress";
import { TankStatus } from "../../../../types/rocketStatusType";

type Props = {
  tankStatus: TankStatus | undefined;
};

export const FuelTankStatus: React.FC<Props> = ({ tankStatus }) => {
  const liquidFuelAmount = tankStatus?.fuel?.amount ?? 0;
  const liquidFuelCapacity = tankStatus?.fuel?.max ?? 0;
  const oxidizerAmount = tankStatus?.lqd_oxygen?.amount ?? 0;
  const oxidizerCapacity = tankStatus?.lqd_oxygen?.max ?? 0;

  // パーセンテージの計算
  const liquidFuelPercentage =
    liquidFuelCapacity > 0 ? (liquidFuelAmount / liquidFuelCapacity) * 100 : 0;
  const oxidizerPercentage =
    oxidizerCapacity > 0 ? (oxidizerAmount / oxidizerCapacity) * 100 : 0;

  return (
    <div className="w-full h-full">
      <h2 className="font-medium">{tankStatus?.fuel?.name ?? "empty fuel"}</h2>
      <LinearProgress variant="determinate" value={liquidFuelPercentage} />
      <p className="text-[0.6rem]">
        {liquidFuelPercentage.toFixed(2)}% {liquidFuelAmount}/
        {liquidFuelCapacity}t
      </p>
      <h2 className="font-medium">{tankStatus?.lqd_oxygen?.name ?? "empty lqdOxygen"}</h2>
      <LinearProgress variant="determinate" value={oxidizerPercentage} />
      <p className="text-[0.6rem]">
        {oxidizerPercentage.toFixed(2)}% {oxidizerAmount}/{oxidizerCapacity}t
      </p>
      <p>temp : {tankStatus?.temperature}</p>
      <p>max temp : {tankStatus?.max_temperature}</p>
    </div>
  );
};
