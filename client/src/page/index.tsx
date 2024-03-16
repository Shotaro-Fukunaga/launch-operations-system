// // App.js

// import { useEffect, useState } from 'react'
// import { Orbital } from '../components/Orbital'
// import { roundToPrecision, truncateToPrecision } from '../utils/common'
// // import Compass from './components/compass'

// export type OrbitalData = {
//   // orbital data
//   apoapsis_altitude: number
//   time_to_apoapsis: number
//   periapsis_altitude: number
//   time_to_periapsis: number
//   eccentricity: number
//   inclination: number
//   period: number
//   semi_major_axis: number

//   // vessel data
//   mean_altitude: number
//   surface_altitude: number
//   vertical_speed: number
//   horizontal_speed: number
// }


// export const Index = () => {
//   // const [heading, setHeading] = useState(0)
//   // const [pitch, setPitch] = useState(0)
//   // const [roll, setRoll] = useState(0)

//   const [data, setData] = useState({
//     apoapsis_altitude: 0,
//     time_to_apoapsis: 0,
//     periapsis_altitude: 0,
//     time_to_periapsis: 0,
//     eccentricity: 0,
//     inclination: 0,
//     period: 0,
//     semi_major_axis: 0,
//     mean_altitude: 0,
//     surface_altitude: 0,
//     vertical_speed: 0,
//     horizontal_speed: 0,
//     heading: 0,
//     pitch: 0,
//     roll: 0,
//   })

//   useEffect(() => {
//     const ws = new WebSocket('ws://localhost:8765')

//     ws.onmessage = (event) => {
//       const message = JSON.parse(event.data)
//       setData(message)
//       // setHeading(message.heading)
//       // setPitch(message.pitch)
//       // setRoll(message.roll)
//     }

//     return () => {
//       ws.close()
//     }
//   }, [])

//   return (
//     <div>
//       {/* <div className="w-[50%] h-[18rem]">
//         <Compass heading={heading} pitch={pitch} roll={roll} />
//       </div> */}
//       <h1>KSP Data</h1>
//       <div className="flex gap-2">
//         <div className="border border-white w-[16rem]">
//           <Orbital data={data} />
//         </div>

//         <div className="border border-white w-[16rem]">
//           <h2>SURFACE</h2>
//           <p>Altitude(Sea Level){roundToPrecision(data.mean_altitude, 1)}m</p>
//           <p>Altitude(Terrain){roundToPrecision(data.surface_altitude, 1)}m</p>
//           <p>Vertical Speed:{roundToPrecision(data.vertical_speed, 2)}m/s</p>
//           <p>
//             Horizontal Speed:{roundToPrecision(data.horizontal_speed, 2)}m/s
//           </p>
//         </div>

//         <div className="border border-white w-[16rem]">
//           <h2>VESSEl</h2>
//           {/* 北を0度 */}
//           <p>Heading {truncateToPrecision(data.heading, 0)}°</p>
//           {/* 機体の回転 角度 */}
//           <p>Roll {truncateToPrecision(data.roll, 0)}</p>
//           <p>Pitch {truncateToPrecision(data.pitch, 0)}</p>
//         </div>
//       </div>
//     </div>
//   )
// }
