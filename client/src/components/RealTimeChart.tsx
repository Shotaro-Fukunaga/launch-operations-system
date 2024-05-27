import { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import "chartjs-adapter-date-fns";

interface Props<T extends { launch_relative_time: number }> {
  data: T[];
  attributeKey: keyof T; 
  attributeName: string; // チャートの軸ラベルに表示される属性名
}

function RealTimeChart<T extends { launch_relative_time: number }>({
  data,
  attributeKey,
  attributeName,
}: Props<T>): JSX.Element {
  const [chartData, setChartData] = useState({
    labels: data.map((item) => item["launch_relative_time"]),
    datasets: [
      {
        label: attributeName,
        data: data.map((item) => item[attributeKey] as number),
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.5)",
      },
    ],
  });

  useEffect(() => {
    const filteredData = data.filter((item) => item.launch_relative_time >= 0);
    setChartData({
      labels: filteredData.map((item) => item["launch_relative_time"]),
      datasets: [
        {
          label: attributeName,
          data: filteredData.map((item) => item[attributeKey] as number),
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.5)",
        },
      ],
    });
  }, [data, attributeKey, attributeName]);

  const options = {
    animation: {
      duration: 0, // アニメーションの持続時間を0に設定して無効化
    },
    scales: {
      x: {
        type: "linear" as const,
        title: {
          display: true,
          text: "X - Time (seconds)",
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
    <div className="w-full h-full">
      <Line options={options} data={chartData} />
    </div>
  );
}

export default RealTimeChart;
