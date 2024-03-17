import { FC } from 'react'

export type EventType = {
  time: string
  name: string
  color?: string;
}

type Props = {
  events?: EventType[]

}

export const EventMarkerGenerator: FC<Props> = ({
  events,
}) => {
  const totalMinutesInDay = 24 * 60 // 1日の総分

  const markers = events?.map((event,index) => {
    const [hours, minutes] = event.time.split(':').map(Number) // "13:00" => [13, 0]
    const eventMinutes = hours * 60 + minutes // イベントの時間を分単位で計算
    const bottomPosition =
      ((totalMinutesInDay - eventMinutes) / totalMinutesInDay) * 100 // 逆順の位置を計算

    const borderColor = event.color ? event.color :"white"
    return (
      <div
        key={index}
        className="h-[2px] w-[14rem] absolute text-white"
        style={{
          backgroundColor: borderColor,
          bottom: `${bottomPosition}%`,
        }}
      >
        <div
          className="h-4 w-4 rounded-full border-2 bg-transparent absolute z-10 top-[-7px] left-[-6.4px]"
          style={{ borderColor: borderColor }}
        />
        <span className="ml-[4rem] text-xs">
          {event.time} - {event.name}
        </span>
      </div>
    )
  })

  return <>{markers}</>
}
