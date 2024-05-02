import { EngineStatus } from "../../../../types/rocketStatusType";

type Props = {
  engineStatus: EngineStatus | undefined;
};

export const RocketEngineStatus: React.FC<Props> = ({ engineStatus }) => {
  return (
    <ul>
      <li>Δv atm: {engineStatus?.atom_delta_v} m/s</li>
      <li>Δv vac: {engineStatus?.vac_delta_v} m/s</li>
      <li>比推力: {engineStatus?.isp} s</li>
      <li>推力: {engineStatus?.max_thrust} kN</li>
      <li>TWR: {engineStatus?.twr}</li>
      <li>重量: {engineStatus?.start_mass} kg</li>
      <li>乾燥重量: {engineStatus?.end_mass} kg</li>
      <li>噴射時間: {engineStatus?.burn_time} s</li>
      <li>温度: {engineStatus?.temperature}</li>
      <li>表面温度: {engineStatus?.max_temperature}</li>
    </ul>
  );
};
