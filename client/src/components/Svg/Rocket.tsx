import React from 'react'

// Propsの型を定義
interface RocketComponentProps {
  fairingFill: string
  firstStageFill: string
  secondStageFill: string
}

const RocketComponent: React.FC<RocketComponentProps> = ({
  fairingFill,
  firstStageFill,
  secondStageFill,
}) => (
  <svg
    width="100%"
    height="100%"
    viewBox="0 -5 46 320"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    {/* フェアリング部分 */}
    <path d="M23.5 0.0L23 0L44.5 26V76H3.5V26Z" fill={fairingFill} />
    {/* 1段目ロケット */}
    <path
      d="M3.5 75 H44.5 V161 H3.5 V75 Z M20.6473 151.9736C21.8484 150.4555 24.1516 150.4555 25.3527 151.9736L35.1752 164.3886C36.7313 166.355 35.3305 169.25 32.8225 169.25H13.1775C10.6695 169.25 9.26867 166.355 10.8248 164.3886L20.6473 151.9736Z"
      fill={firstStageFill}
    />
    {/* 2段目ロケット */}
    <path
      d="M3.696 160H44.5V297H3.5V160ZM20.4405 286.365C21.9836 283.604 26.0114 283.604 27.5544 286.365L38.7055 306.321C40.1952 308.987 38.2375 312.25 35.1486 312.25H12.8464C9.7574 312.25 7.7997 308.987 9.2894 306.321L20.4405 286.365ZM19.9655 214.9437C21.836 211.2586 27.174 211.2586 29.0445 214.9437L63.4676 282.764C65.155 286.088 62.701 290 58.9281 290H-10.91809C-14.69102 290 -17.14497 286.088 -15.45761 282.764L19.9655 214.9437Z"
      fill={secondStageFill}
    />
  </svg>
)

export default RocketComponent
