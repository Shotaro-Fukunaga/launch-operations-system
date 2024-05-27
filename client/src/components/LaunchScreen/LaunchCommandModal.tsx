import { useState, FC } from "react";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import CloseIcon from "@mui/icons-material/Close";
type Props = {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (command: CommandType) => void;
};

export type CommandType = {
  launch_date: Date;
  command: string;
  target_orbit: {
    periapsis: number;
    apoapsis: number;
    inclination: number;
    speed: number;
  };
};

// 現在の日付と時刻を "YYYY-MM-DDTHH:MM" フォーマットで取得する関数
const getCurrentDateTime = () => {
  const now = new Date();
  now.setMinutes(now.getMinutes() + 1); // 現在の時刻に1分を追加
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};

const LaunchCommandModal: FC<Props> = ({ isOpen, onClose, onSubmit }) => {
  const [launchDate, setLaunchDate] = useState(getCurrentDateTime());
  const [periapsis, setPeriapsis] = useState(400000);
  const [apoapsis, setApoapsis] = useState(400000);
  const [inclination, setInclination] = useState(51.6);
  const [speed, setSpeed] = useState(7660);

  const handleSubmit = () => {
    const command: CommandType = {
      launch_date: new Date(launchDate),
      command: "sequence",
      target_orbit: { periapsis, apoapsis, inclination, speed },
    };
    onSubmit(command);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="relative p-5 bg-gray-600 rounded shadow-lg z-60 w-[30%] text-white">
        <button
          onClick={onClose}
          className="absolute top-0 right-0 mt-2 mr-2 bg-gray-600"
        >
          <CloseIcon />
        </button>
        <h2 className="mb-4 text-[2rem] text-center font-bold">
          Launch Sequence Settings
        </h2>

        <div className="flex justify-center w-full p-5 gap-[2rem]">
          <div className="text-center">
            <h2 className="font-bold">機体情報</h2>
            <p>機体名：Foward1.7</p>
            <p>機体種別: Rocket</p>
            <p>ペイロード: 430 kg</p>
            <p>機体高さ：21.9m</p>
            <p>機体全長：2.1m</p>
            <p>機体直径：2.1m</p>
            <p>重量：43.099t</p>
            <p>乾燥重量：16.218t</p>
          </div>
          <div className="text-center">
            <h2 className="font-bold">発射地点</h2>
            <p>種子島宇宙センター</p>
            <p>緯度 : 31.2°</p>
            <p>経度 : 130.9°</p>
          </div>
        </div>

        <div className="mb-4">
          <label className="block ">Launch Date:</label>
          <input
            type="datetime-local"
            value={launchDate}
            onChange={(e) => setLaunchDate(e.target.value)}
            className="w-full px-2 py-1 rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block ">Periapsis:</label>
          <input
            type="number"
            value={periapsis}
            onChange={(e) => setPeriapsis(Number(e.target.value))}
            className="w-full px-2 py-1 rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block ">Apoapsis:</label>
          <input
            type="number"
            value={apoapsis}
            onChange={(e) => setApoapsis(Number(e.target.value))}
            className="w-full px-2 py-1 rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block ">Inclination:</label>
          <input
            type="number"
            value={inclination}
            onChange={(e) => setInclination(Number(e.target.value))}
            className="w-full px-2 py-1 rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block ">Speed:</label>
          <input
            type="number"
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
            className="w-full px-2 py-1 rounded"
          />
        </div>
        <div className="flex justify-center">
          <button
            onClick={handleSubmit}
            className="px-4 py-2 text-white bg-red-500 rounded"
          >
            <RocketLaunchIcon />
            Sequence start
          </button>
        </div>
      </div>
    </div>
  );
};

export default LaunchCommandModal;
