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
  return (
    <div className="w-full h-full">
      <div className="bg-gray-600 text-center">
        <h2 className="font-bold text-[0.6rem]">{title}</h2>
      </div>
      <div className="p-[0.4rem] space-y-[0.1rem]">
        <p>
          Temp: {calcAverage(fairing1?.temperature, fairing2?.temperature)}
          °C
        </p>
        <p>
          Max Temp:{" "}
          {calcAverage(fairing1?.max_temperature, fairing2?.max_temperature)}
          °C
        </p>
        <p>
          Dyn Press:{" "}
          {calcAverage(fairing1?.dynamic_pressure, fairing2?.dynamic_pressure)}{" "}
          Pa
        </p>

        <StatusLabel
          status={fairing1?.status}
          customLabels={{ 3: "Jettisoned" }}
        />
      </div>
    </div>
  );
};
