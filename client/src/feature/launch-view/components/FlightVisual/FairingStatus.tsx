import { FairingStatusType } from "../../../../types/rocketStatusType";
import StatusLabel from "./StatusLabel";

type Props = {
  title: string;
  fairing1?: FairingStatusType;
  fairing2?: FairingStatusType;
};

export const FairingStatus: React.FC<Props> = ({
  fairing1,
  fairing2,
  title,
}) => {
  const calcAverage = (value1?: number, value2?: number) => {
    let total = 0;
    let count = 0;

    if (value1 !== undefined) {
      total += value1;
      count++;
    }

    if (value2 !== undefined) {
      total += value2;
      count++;
    }

    if (count === 0) return 0;
    return (total / count).toFixed(1);
  };

  const temp = calcAverage(fairing1?.temperature, fairing2?.temperature);
  const maxTemp = calcAverage(
    fairing1?.max_temperature,
    fairing2?.max_temperature
  );
  const dynPress = calcAverage(
    fairing1?.dynamic_pressure,
    fairing2?.dynamic_pressure
  );
  return (
    <div className="w-full h-full text-[0.6rem] border border-gray-400">
      <div className="text-center bg-gray-600">
        <h2 className="font-bold">{title}</h2>
      </div>
      <ul className="p-[0.4rem] space-y-[0.1rem]">
        <li>Temp: {temp} / {maxTemp} °C</li>
        <li>Dyn Press: {dynPress} Pa</li>
        <li>
          <StatusLabel
            status={fairing1?.status}
            customLabels={{ 3: "Jettisoned" }}
          />
        </li>
      </ul>
    </div>
  );
};
