import { EngineStatus } from "../../../../types/rocketStatusType";
import StatusLabel from "./StatusLabel";

type Props = {
  title: string;
  engineStatus: EngineStatus | undefined;
};

export const RocketEngineStatus: React.FC<Props> = ({
  title,
  engineStatus,
}) => {
  return (
    <div className="h-full w-full text-[0.6rem] border border-gray-400">
      <div className="text-center bg-gray-600">
        <h2 className="font-bold ">{title}</h2>
      </div>
      <ul className="p-[0.4rem] space-y-[0.1rem]">
        <li>Δv atm: {engineStatus?.atom_delta_v} m/s</li>
        <li>Δv vac: {engineStatus?.vac_delta_v} m/s</li>
        <li>比推力: {engineStatus?.isp} s</li>
        <li>推力: {engineStatus?.max_thrust} kN</li>
        <li>TWR: {engineStatus?.twr}</li>
        <li>重量: {engineStatus?.start_mass} kg</li>
        <li>乾燥重量: {engineStatus?.end_mass} kg</li>
        <li>噴射時間: {engineStatus?.burn_time} s</li>
        <li>
          Temp: {engineStatus?.temperature} / {engineStatus?.max_temperature} °C
        </li>

        <li>
          <StatusLabel
            status={engineStatus?.status}
            customLabels={{ 1: "Burning" }}
          />
        </li>
      </ul>
    </div>
  );
};
