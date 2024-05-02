import RocketComponent from "../../../../components/Svg/Rocket";

import { useContext } from "react";
import { RocketEngineStatus } from "./Delta_V_Status";
import { FuelTankStatus } from "./FuelTankStatus";
import { WebSocketContext } from "../../../../context/WebSocketContext";

export const FlightVisualizer = () => {
  const webSocketContext = useContext(WebSocketContext);
  if (!webSocketContext) {
    return <div>Loading...</div>;
  }
  const { messages } = webSocketContext;
  const { rocketStatus } = messages;

  return (
    <>
      <div className="flex w-full h-full">
        <div className="h-full w-[30%] text-[0.6rem] flex flex-col">
          <div className="h-[25%] w-full border border-gray-400 px-[0.6rem]">
            <p>フェアリング</p>
            <h2 className="font-medium">Status :</h2>
            <p className={`rounded-md bg-green-300`}>
              {/* {unitStatus?.["fairing_1"]} */}
            </p>
            <p>温度: </p>
            <p>最大許容温度: </p>
          </div>

          <div className="h-[37.5%] w-full border border-gray-400 flex flex-col px-[0.6rem]">
            <p>Second Tank</p>
            <FuelTankStatus tankStatus={rocketStatus?.second_tank} />
          </div>

          <div className="h-[37.5%] w-full border border-gray-400 px-[0.6rem]">
            <p>Main Tank</p>
            <FuelTankStatus tankStatus={rocketStatus?.main_tank} />
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
          <div className="h-[25%] w-full  border border-gray-400">
            {/* TODO */}
            <p>ペイロード</p>
            <p>質量:3 kg</p>
            {/* <p>アンテナ</p>
            <p>{rocketStatus?.payload_status.anttena.power}</p>
            <p>{rocketStatus?.payload_status.anttena.packet_interval}</p>
            <p>{rocketStatus?.payload_status.anttena.packet_size}</p>
            <p>{rocketStatus?.payload_status.anttena.packet_resource_cost}</p>

            <p>バス</p>
            <p>{rocketStatus?.payload_status.satellite_bus.shielded}</p>
            <p>{rocketStatus?.payload_status.satellite_bus.current_charge}</p>
            <p>{rocketStatus?.payload_status.satellite_bus.max_charge}</p>

            <p>ソーラーパネル</p>
            <p>右{rocketStatus?.payload_status.solar_panel_1.energy_flow}</p>
            <p>右{rocketStatus?.payload_status.solar_panel_1.sun_exposure}</p>
            <p>左{rocketStatus?.payload_status.solar_panel_2.energy_flow}</p>
            <p>左{rocketStatus?.payload_status.solar_panel_2.sun_exposure}</p>

            <p>リアクションホイール</p>
            <p>{rocketStatus?.payload_status.reaction_wheel.active}</p> */}
          </div>

          <div className="h-[37.5%] w-full  border border-gray-400 px-[0.6rem]">
            <p>Second Engine Status</p>
            <RocketEngineStatus engineStatus={rocketStatus?.second_engine} />
          </div>

          <div className="h-[37.5%] w-full  border border-gray-400 px-[0.6rem]">
            <p>Main Engine Status</p>
            <RocketEngineStatus engineStatus={rocketStatus?.main_engine} />
          </div>
        </div>
      </div>
    </>
  );
};
