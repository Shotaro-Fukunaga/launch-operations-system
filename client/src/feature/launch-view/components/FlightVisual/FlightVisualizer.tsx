import RocketComponent from '../../../../components/Svg/Rocket'

import { RocketEngineStatus } from './RocketEngineStatus'
import { RocketFuelStatus } from './RocketFuelStatus'
import { RocketStatus } from './RocketStatus'

export const FlightVisualizer = () => {
  return (
    <>
      <div className="flex w-full h-full">
        <div className="h-full w-[30%] border border-blue-300 flex flex-col text-[0.6rem]">
          <div className="h-[25%] w-full  border border-gray-400"></div>
          <div className="h-[30%] w-full  border border-gray-400">
            <RocketEngineStatus
              deltaV={4500}
              specificImpulse={300}
              thrust={100}
              twr={1.5}
              weight={5000}
              dryWeight={3000}
              burnTime={60}
            />
          </div>
          <div className="h-[45%] w-full  border border-gray-400">
            <RocketEngineStatus
              deltaV={4500}
              specificImpulse={300}
              thrust={100}
              twr={1.5}
              weight={5000}
              dryWeight={3000}
              burnTime={60}
            />
          </div>
        </div>
        <div className="h-full w-[30%]">
          <RocketComponent
            fairingFill={'#E97A19'}
            firstStageFill={'#46F610BF'}
            secondStageFill={'#8E8E8E93'}
          />
        </div>
        <div className="h-full w-[40%] border border-blue-300 text-[0.6rem] flex flex-col">
          <div className="h-[25%] w-full flex gap-4 border border-gray-400">
            <div className="w-[50%] h-full">
              {/* <RocketFuelStatus
                liquidFuelAmount={3000}
                liquidFuelCapacity={5000}
                oxidizerAmount={3000}
                oxidizerCapacity={5000}
              /> */}
            </div>
            <div className="w-[50%] h-full">
              <RocketStatus
                temperature={200}
                dynamicPressure={5}
                status="Burn"
              />
            </div>
          </div>

          <div className="h-[30%] w-full flex gap-4 border border-gray-400">
            <div className="w-[50%] h-full">
              <RocketFuelStatus
                liquidFuelAmount={3000}
                liquidFuelCapacity={5000}
                oxidizerAmount={3000}
                oxidizerCapacity={5000}
              />
            </div>
            <div className="w-[50%] h-full">
              <RocketStatus
                temperature={200}
                dynamicPressure={5}
                status="Burn"
              />
            </div>
          </div>

          <div className="h-[45%] w-full flex gap-4">
            <div className="w-[50%] h-full">
              <RocketFuelStatus
                liquidFuelAmount={3000}
                liquidFuelCapacity={5000}
                oxidizerAmount={3000}
                oxidizerCapacity={5000}
              />
            </div>
            <div className="w-[50%] h-full">
              <RocketStatus
                temperature={200}
                dynamicPressure={5}
                status="Burn"
              />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
