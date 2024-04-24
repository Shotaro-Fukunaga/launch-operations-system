import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface Props {
  labels: string[];
  datasetLabel: string;
  chartTitle?: string;
  data: number[];
  fillColor: string;
  borderColor: string;
  xGridColor?: string; // X軸グリッド線の色
  yGridColor?: string; // Y軸グリッド線の色
}

export const DynamicLineChart = ({
  labels,
  datasetLabel,
  chartTitle,
  data,
  fillColor,
  borderColor,
  xGridColor,
  yGridColor,
}: Props) => {
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: datasetLabel,
        data: data,
        fill: false,
        backgroundColor: fillColor,
        borderColor: borderColor,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: chartTitle,
      },
    },
    scales: {
      x: {
        grid: {
          color: xGridColor,
        },
      },
      y: {
        min: 0,
        max: 400000, // 最大400km
        grid: {
          color: yGridColor,
        },
      },
    },
  };

  return (
    <div className="h-full w-full">
      <Line data={chartData} options={options} />
    </div>
  );
};
