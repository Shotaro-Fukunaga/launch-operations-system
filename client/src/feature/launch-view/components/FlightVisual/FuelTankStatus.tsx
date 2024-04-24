import React from 'react'
import LinearProgress from '@mui/material/LinearProgress'

type Props = {
  liquidFuelAmount: number
  liquidFuelCapacity: number
  oxidizerAmount: number
  oxidizerCapacity: number
}

export const FuelTankStatus: React.FC<Props> = ({
  liquidFuelAmount,
  liquidFuelCapacity,
  oxidizerAmount,
  oxidizerCapacity,
}) => {
  const liquidFuelPercentage = (liquidFuelAmount / liquidFuelCapacity) * 100
  const oxidizerPercentage = (oxidizerAmount / oxidizerCapacity) * 100

  return (
    <div className="w-full h-full">
      
      <h2 className="font-medium">LiquidFuel</h2>
      <LinearProgress variant="determinate" value={liquidFuelPercentage} />
      <p className="text-[0.6rem]">
        {liquidFuelPercentage.toFixed(2)}% {liquidFuelAmount}/
        {liquidFuelCapacity}t
      </p>
      <h2 className="font-medium">Oxidizer</h2>
      <LinearProgress variant="determinate" value={oxidizerPercentage} />
      <p className="text-[0.6rem]">
        {oxidizerPercentage.toFixed(2)}% {oxidizerAmount}/{oxidizerCapacity}t
      </p>
    </div>
  )
}
