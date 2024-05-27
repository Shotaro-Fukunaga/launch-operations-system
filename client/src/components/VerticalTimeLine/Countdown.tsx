// import { useState, useEffect, FC } from 'react'

// type Props = {
//   launchDateTime: Date
// }
// export const Countdown: FC<Props> = ({ launchDateTime }) => {
//   const [currentDateTime, setCurrentDateTime] = useState(new Date())

//   useEffect(() => {
//     const timer = setInterval(() => {
//       setCurrentDateTime(new Date())
//     }, 1000)
//     return () => clearInterval(timer)
//   }, [])

//   // Xを計算
//   const calculateX = (currentDateTime: Date): string => {
//     const differenceInSeconds =
//       (launchDateTime.getTime() - currentDateTime.getTime()) / 1000
//     const sign = differenceInSeconds < 0 ? '+' : '-'
//     const absSeconds = Math.abs(differenceInSeconds)
//     const days = Math.floor(absSeconds / (60 * 60 * 24))
//     const hours = Math.floor((absSeconds % (60 * 60 * 24)) / (60 * 60))
//     const minutes = Math.floor((absSeconds % (60 * 60)) / 60)
//     const seconds = Math.floor(absSeconds % 60)

//     return `${sign}${String(days * 24 + hours).padStart(2, '0')}:${String(
//       minutes
//     ).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
//   }
//   const x = calculateX(currentDateTime)

//   const formatLaunchDateTime = launchDateTime.toLocaleString('ja-JP', {
//     year: 'numeric',
//     month: '2-digit',
//     day: '2-digit',
//     hour: '2-digit',
//     minute: '2-digit',
//     second: '2-digit',
//   })

//   // 現在の日本時間をフォーマット
//   const formatCurrentJSTDateTime = currentDateTime.toLocaleString('ja-JP', {
//     year: 'numeric',
//     month: '2-digit',
//     day: '2-digit',
//     hour: '2-digit',
//     minute: '2-digit',
//     second: '2-digit',
//     timeZone: 'Asia/Tokyo',
//   })

//   // 現在のUTC時間をフォーマット
//   // const formatCurrentUTCDateTime = currentDateTime.toLocaleString('ja-JP', {
//   //   year: 'numeric',
//   //   month: '2-digit',
//   //   day: '2-digit',
//   //   hour: '2-digit',
//   //   minute: '2-digit',
//   //   second: '2-digit',
//   //   timeZone: 'UTC',
//   // })

//   return (
//     <>
//       <div>j: {formatCurrentJSTDateTime}</div>
//       {/* <div>utc: {formatCurrentUTCDateTime}</div> */}
//       <div>γ: {formatLaunchDateTime}</div>
//       <div>x: {x}</div>
//     </>
//   )
// }
