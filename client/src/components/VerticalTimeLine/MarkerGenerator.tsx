// import { FC } from 'react'


// // TODO 日付が今日ならリアルタイムで進行、過去なら100%、未来なら0%にする
// const MarkerGenerator: FC = () => {
//   const totalMinutes = 24 * 60 // 1日の総分

//   const markers = Array.from({ length: totalMinutes }, (_, minute) => {
//     const bottomPosition = ((totalMinutes - minute) / totalMinutes) * 100
//     const isHourMarker = minute % 60 === 0
//     return (
//       <div
//         key={minute}
//         className="absolute bg-gray-600"
//         style={{
//           height: '2px',
//           width: isHourMarker ? '3.6rem' : '0.6rem',
//           bottom: `${bottomPosition}%`,
//           right: '100%',
//         }}
//       >
//         {isHourMarker && (
//           <span className="mr-4 text-xs text-white">
//             {(Math.floor(minute / 60) % 24).toString().padStart(2, '0')}:00
//           </span>
//         )}
//       </div>
//     )
//   })

//   return <>{markers}</>
// }

// export default MarkerGenerator
