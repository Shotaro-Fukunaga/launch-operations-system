type Props = {
  deltaV: number
  specificImpulse: number
  thrust: number
  twr: number // Thrust-to-Weight Ratio
  weight: number
  dryWeight: number
  burnTime: number
}

export const RocketEngineStatus: React.FC<Props> = ({
  deltaV,
  specificImpulse,
  thrust,
  twr,
  weight,
  dryWeight,
  burnTime,
}) => {
  return (
    <ul>
      <li>Δv: {deltaV} m/s</li>
      <li>比推力: {specificImpulse} s</li>
      <li>推力: {thrust} kN</li>
      <li>TWR: {twr}</li>
      <li>重量: {weight} kg</li>
      <li>乾燥重量: {dryWeight} kg</li>
      <li>噴射時間: {burnTime} s</li>
    </ul>
  )
}
