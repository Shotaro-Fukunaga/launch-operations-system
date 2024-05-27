import { FC } from 'react'
import { EventRecord } from '../../../../types/flightRecordType';


type Props = {
  events?: EventRecord[]

}

export const EventMarkerGenerator: FC<Props> = ({
  events,
}) => {
  const totalMinutesInDay = 24 * 60 // 1日の総分

  const getColorForEventLevel = (level: number) => {
    switch (level) {
      case 0:
        return 'gray'; // 通常
      case 1:
        return 'blue'; // 重要
      case 2:
        return 'red'; // エラー
      default:
        return 'white'; // 未定義のレベル
    }
  }

  const markers = events?.map((event, index) => {
    const eventDate = new Date(event.time);
    const hours = eventDate.getHours();
    const minutes = eventDate.getMinutes();
    const eventMinutes = hours * 60 + minutes; // イベントの時間を分単位で計算
    const bottomPosition =
      ((totalMinutesInDay - eventMinutes) / totalMinutesInDay) * 100 // 逆順の位置を計算

    const borderColor = getColorForEventLevel(event.event_level);
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
        {`${hours}:${minutes < 10 ? '0' + minutes : minutes}`} - {event.event_type}
        </span>
      </div>
    )
  })

  return <>{markers}</>
}
