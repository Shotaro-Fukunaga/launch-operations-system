import React from 'react'

type RocketStatusProps = {
  temperature: number // 温度を数値で
  dynamicPressure: number // 動的圧力を数値で
  status: 'Cut OFF' | 'Burn' | 'Deployment' // ステータスを限定する
}

export const RocketStatus: React.FC<RocketStatusProps> = ({
  temperature,
  dynamicPressure,
  status,
}) => {
  // ステータスに応じた背景色を設定
  const statusBackgroundColor = {
    'Cut OFF': 'bg-gray-500', // 灰色で「停止」状態を示す
    Burn: 'bg-red-500', // 赤色で「燃焼」状態を示す
    Deployment: 'bg-green-500', // 緑色で「展開」状態を示す
  }

  return (
    <div>
      <h2 className="font-medium">Temperature :</h2>
      <p>{temperature}°</p>

      <h2 className="font-medium">Pressure :</h2>
      <p>{dynamicPressure} hPa</p>

      <h2 className="font-medium">Status :</h2>
      <p className={`rounded-md ${statusBackgroundColor[status]}`}>{status}</p>
    </div>
  )
}
