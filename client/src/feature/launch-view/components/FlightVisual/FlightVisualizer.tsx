import RocketComponent from "../../../../components/Svg/Rocket";

import { RocketEngineStatus } from "./Delta_V_Status";
import { FuelTankStatus } from "./FuelTankStatus";

export const FlightVisualizer = () => {
  return (
    <>
      <div className="flex w-full h-full">
        <div className="h-full w-[30%] text-[0.6rem] flex flex-col">
          <div className="h-[25%] w-full border border-gray-400 px-[0.6rem]">
            <p>フェアリング</p>
            <h2 className="font-medium">Status :</h2>
            <p className={`rounded-md bg-green-300`}>Deployed</p>
            <p>温度</p>
            <p>表面温度</p>
            <p>圧力</p>
          </div>

          <div className="h-[37.5%] w-full border border-gray-400 flex flex-col px-[0.6rem]">
            <p>第一タンク</p>
            <p>温度</p>
            <p>表面温度</p>
            <FuelTankStatus
              liquidFuelAmount={3000}
              liquidFuelCapacity={5000}
              oxidizerAmount={3000}
              oxidizerCapacity={5000}
            />
          </div>

          <div className="h-[37.5%] w-full border border-gray-400 px-[0.6rem]">
            <p>第２タンク</p>
            <p>温度</p>
            <p>表面温度</p>
            <FuelTankStatus
              liquidFuelAmount={3000}
              liquidFuelCapacity={5000}
              oxidizerAmount={3000}
              oxidizerCapacity={5000}
            />
          </div>
        </div>

        <div className="h-full w-[30%] flex-col content-end">
          <RocketComponent
            fairingFill={"#E97A19"}
            firstStageFill={"#46F610BF"}
            secondStageFill={"#8E8E8E93"}
          />
        </div>

        <div className="h-full w-[40%] flex flex-col text-[0.6rem]">
          {/* Payload and Satelite Bus */}
          <div className="h-[25%] w-full  border border-gray-400"></div>

          <div className="h-[37.5%] w-full  border border-gray-400 px-[0.6rem]">
            <p>第一エンジン</p>
            <RocketEngineStatus
              deltaV={4500}
              specificImpulse={300}
              thrust={100}
              twr={1.5}
              weight={5000}
              dryWeight={3000}
              burnTime={60}
              temperature={300}
              skinTemperature={300}
            />
          </div>

          <div className="h-[37.5%] w-full  border border-gray-400 px-[0.6rem]">
            <p>第２エンジン</p>
            <RocketEngineStatus
              deltaV={4500}
              specificImpulse={300}
              thrust={100}
              twr={1.5}
              weight={5000}
              dryWeight={3000}
              burnTime={60}
              temperature={300}
              skinTemperature={300}
            />
          </div>
        </div>
      </div>
    </>
  );
};
