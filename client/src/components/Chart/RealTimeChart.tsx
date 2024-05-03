import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import "chartjs-adapter-date-fns";

interface RealTimeChartProps<T extends { time: string }> {
  data: T[];
  attributeKey: keyof T; // T型の任意のキー
  attributeName: string; // チャートの軸ラベルに表示される属性名
}

function RealTimeChart<T extends { time: string }>({
  data,
  attributeKey,
  attributeName,
}: RealTimeChartProps<T>): JSX.Element {
  const [chartData, setChartData] = useState({
    labels: data.map((item) => item["time"]),
    datasets: [
      {
        label: attributeName,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        data: data.map((item) => item[attributeKey] as any), // 型の一般性を保持しつつ、anyにアサーション
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.5)",
      },
    ],
  });

  useEffect(() => {
    setChartData({
      labels: data.map((item) => item["time"]),
      datasets: [
        {
          label: attributeName,
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          data: data.map((item) => item[attributeKey] as any), // 更新時にも同様にアサーション
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.5)",
        },
      ],
    });
  }, [data, attributeKey, attributeName]);

  const options = {
    scales: {
      x: {
        type: "time" as const,
        time: {
          unit: "second" as const,
          displayFormats: {
            second: "MMM dd, yyyy HH:mm:ss",
          },
        },
        title: {
          display: true,
          text: "Time",
        },
      },
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: attributeName,
        },
      },
    },
  };

  return (
    <div className="h-full w-full">
      <Line options={options} data={chartData} />
    </div>
  );
}

export default RealTimeChart;
