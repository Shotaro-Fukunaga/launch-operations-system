import { useState, useEffect } from "react";

// 気象データを模擬するためのダミーデータ
const mockWeatherData = {
  windSurface: {
    // 地表の風
    speed: 5, // 風速 (m/s)
    direction: 180, // 風向 (度)
  },
  windUpper: {
    // 高層風
    speed: 20, // 風速 (m/s)
    direction: 270, // 風向 (度)
    altitude: 10000, // 高度 (m)
  },
  thunder: {
    intensity: 3, // 雷の強さ
    frequency: 1, // 頻度 (1低 - 5高)
  },
  clouds: {
    type: "Stratus", // 雲の種類
    coverage: 50, // 雲の覆い (%)
  },
  rain: {
    intensity: 2, // 雨の強さ (1低 - 5高)
  },
};

function WeatherInfo() {
  const [weatherData, setWeatherData] = useState(mockWeatherData);

  useEffect(() => {
    // 実際のアプリケーションではここでAPIから気象データを取得します
    setWeatherData(mockWeatherData);
  }, []);

  return (
    <div className="h-full w-full text-[1rem]">
      <h2>気象情報</h2>
      <div>
        <h2>地表の風情報</h2>
        <p>風速: {weatherData.windSurface.speed} m/s</p>
        <p>風向: {weatherData.windSurface.direction} degrees</p>
      </div>
      <div>
        <h2>高層風情報</h2>
        <p>風速: {weatherData.windUpper.speed} m/s</p>
        <p>風向: {weatherData.windUpper.direction} degrees</p>
        <p>高度: {weatherData.windUpper.altitude} m</p>
      </div>
      <div>
        <h2>雷情報</h2>
        <p>強度: {weatherData.thunder.intensity}</p>
        <p>発生頻度: {weatherData.thunder.frequency}</p>
      </div>
      <div>
        <h2>雲情報</h2>
        <p>種類: {weatherData.clouds.type}</p>
        <p>雲量: {weatherData.clouds.coverage}%</p>
      </div>
      {/* <div>
        <h2>雨情報</h2>
        <p>強度: {weatherData.rain.intensity}</p>
      </div> */}
    </div>
  );
}

export default WeatherInfo;
