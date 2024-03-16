import React from 'react'
import ReactPlayer from 'react-player'

export const LivePlayer = () => {
  return (
    <div className="player-wrapper">
      <ReactPlayer
        url="http://localhost:8000/live/programming/index.m3u8"
        width="100%"
        height="100%"
        controls={true}
      />
    </div>
  )
}
