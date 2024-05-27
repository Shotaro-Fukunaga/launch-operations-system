// import { useState, useEffect, FC } from "react";



// function generateTimeline(
//   launchTime: Date,
//   launchCompleteTime: Date,
//   startTime: Date
// ) {
//   // startTimeからlaunchTimeまでの秒数（通常は負の値）
//   const startOffsetSeconds =
//     (startTime.getTime() - launchTime.getTime()) / 1000;
//   // launchTimeからlaunchCompleteTimeまでの秒数
//   const totalLaunchDuration =
//     (launchCompleteTime.getTime() - launchTime.getTime()) / 1000;

//   // 総秒数の計算: startOffsetSecondsの絶対値 + launchTimeからlaunchCompleteTimeまでの秒数
//   const totalDuration = Math.abs(startOffsetSeconds) + totalLaunchDuration;

//   // 時間差に基づいて配列を生成
//   const timelineArray = Array.from(
//     { length: totalDuration + 1 },
//     (_, index) => {
//       const secondsFromStart = startOffsetSeconds + index; // startTimeからの経過秒数（負の値からスタート）
//       const currentTime = new Date(startTime.getTime() + index * 1000);

//       // 時間の表示フォーマット
//       const formatTime = (time: number) => {
//         const prefix = time < 0 ? "x - " : "x + ";
//         const absTime = Math.abs(time);
//         const hours = Math.floor(absTime / 3600);
//         const minutes = Math.floor((absTime % 3600) / 60);
//         const seconds = absTime % 60;
//         return `${prefix}${hours.toString().padStart(2, "0")}:${minutes
//           .toString()
//           .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
//       };

//       // 日付と時間の表示をISO 8601形式で
//       const formatDate = (date: Date) => {
//         const isoString = date.toISOString(); // ISO 8601形式の文字列を取得
//         const formattedDate =
//           isoString.replace("T", " ").slice(0, 19) + "+00:00"; // "T"を空白に置換し、秒までを表示しタイムゾーンを追加
//         return formattedDate;
//       };

//       return {
//         x: formatTime(secondsFromStart),
//         utc: formatDate(currentTime),
//         jst: currentTime.toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" }),
//       };
//     }
//   );

//   return timelineArray;
// }


// const data = [
//   { x: "x - 00:00:05", utc: "2024-05-03 01:59:55+00:00", jst: "2024/5/3 10:59:55" },
//   { x: "x - 00:00:04", utc: "2024-05-03 01:59:56+00:00", jst: "2024/5/3 10:59:56" },
//   { x: "x - 00:00:03", utc: "2024-05-03 01:59:57+00:00", jst: "2024/5/3 10:59:57" },
//   { x: "x - 00:00:02", utc: "2024-05-03 01:59:58+00:00", jst: "2024/5/3 10:59:58" },
//   { x: "x - 00:00:01", utc: "2024-05-03 01:59:59+00:00", jst: "2024/5/3 10:59:59" },
//   { x: "x + 00:00:00", utc: "2024-05-03 02:00:00+00:00", jst: "2024/5/3 11:00:00" },
//   { x: "x + 00:00:01", utc: "2024-05-03 02:00:01+00:00", jst: "2024/5/3 11:00:01" },
//   { x: "x + 00:00:02", utc: "2024-05-03 02:00:02+00:00", jst: "2024/5/3 11:00:02" },
//   { x: "x + 00:00:03", utc: "2024-05-03 02:00:03+00:00", jst: "2024/5/3 11:00:03" },
//   { x: "x + 00:00:04", utc: "2024-05-03 02:00:04+00:00", jst: "2024/5/3 11:00:04" },
//   { x: "x + 00:00:05", utc: "2024-05-03 02:00:05+00:00", jst: "2024/5/3 11:00:05" },
// ];


// export const TimelineBar: FC = () => {
//   const markers = data.map((item, index) => (
//     <div
//       key={index}
//       className="absolute bg-blue-500"
//       style={{
//         height: "2px",
//         width: "4.6rem",
//         bottom: `${((data.length - 1 - index) / (data.length - 1)) * 100}%`,
//         right: "100%",
//       }}
//     >
//       <span className="text-xs text-white">{item.x}</span>
//     </div>
//   ));

//   return (
//     <div className="relative w-full h-full">
//       <div className="overflow-auto h-full w-full pl-[12rem]" style={{ scrollbarWidth: 'none' }}>
//         {/* スタイルシートを用いてスクロールバーを非表示にする */}
//         <style>
//           {`
//             .overflow-auto::-webkit-scrollbar {
//               display: none; /* Chrome, Safari, Opera */
//             }
//             .overflow-auto {
//               -ms-overflow-style: none; /* IE and Edge */
//               scrollbar-width: none; /* Firefox */
//             }
//           `}
//         </style>
//         <div className="relative h-full">
//           {markers}
//         </div>
//       </div>
//       <div
//         className="absolute w-1 h-full bg-gray-600"
//         style={{ top: 0, left: "12rem" }}
//       />
//     </div>
//   );
// };
