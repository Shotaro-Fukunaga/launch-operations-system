import { useState, useEffect } from "react";

// 気象データを模擬するためのダミーデータ
const mockWeatherData = {
  temperature: {
    current: 22, // 現在の気温 (°C)
    high: 30, // 最高気温 (°C)
    low: 15, // 最低気温 (°C)
  },
  humidity: 70, // 湿度 (%)
  pressure: 1013, // 気圧 (hPa)
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
    intensity: 3, // 雨量 mm/h
    probability: 20, // 降水確率 (%)
  },
};

function WeatherInfo() {
  const [weatherData, setWeatherData] = useState(mockWeatherData);

  useEffect(() => {
    // 実際のアプリケーションではここでAPIから気象データを取得する想定。
    // 高層風のデータが取得できるAPIが有料だったため、ダミーデータを使用
    setWeatherData(mockWeatherData);
  }, []);

  return (
    <div className="h-full w-full text-[0.8rem]">
      <div className="flex justify-center w-full bg-gray-600">
        <h2 className="font-bold">Wheather Info</h2>
      </div>

      <div className="flex gap-[1rem] px-[1rem] py-[0.4rem]">
        <div className="flex flex-col gap-[0.4rem]">
          <div>
            <h2 className="font-semibold">基本情報</h2>
            <p>現在の気温: {weatherData.temperature.current} °C</p>
            <p>最高気温: {weatherData.temperature.high} °C</p>
            <p>最低気温: {weatherData.temperature.low} °C</p>
            <p>湿度: {weatherData.humidity} %</p>
            <p>気圧: {weatherData.pressure} hPa</p>
          </div>
          <div>
            <h2 className="font-semibold">地表風情報</h2>
            <p>風速: {weatherData.windSurface.speed} m/s</p>
            <p>風向: {weatherData.windSurface.direction} degrees</p>
          </div>
          <div>
            <h2 className="font-semibold">高層風情報</h2>
            <p>風速: {weatherData.windUpper.speed} m/s</p>
            <p>風向: {weatherData.windUpper.direction} degrees</p>
            <p>高度: {weatherData.windUpper.altitude} m</p>
          </div>
        </div>

        <div className="flex flex-col gap-[0.4rem]">
          <div>
            <h2 className="font-semibold">雷情報</h2>
            <p>強度: {weatherData.thunder.intensity}</p>
            <p>発生頻度: {weatherData.thunder.frequency}</p>
          </div>
          <div>
            <h2 className="font-semibold">雲情報</h2>
            <p>種類: {weatherData.clouds.type}</p>
            <p>雲量: {weatherData.clouds.coverage}%</p>
          </div>
          <div>
            <h2 className="font-semibold">雨情報</h2>
            <p>雨量: {weatherData.rain.intensity} mm/h</p>
            <p>降水確率: {weatherData.rain.probability}%</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WeatherInfo;
