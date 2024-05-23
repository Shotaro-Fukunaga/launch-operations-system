import React, { useState } from "react";
import { VesselTelemetryType } from "../../../types/vesselTelemetryType";

interface VesselTelemetryViewerProps {
  telemetryData?: VesselTelemetryType;
}

const VesselTelemetryViewer: React.FC<VesselTelemetryViewerProps> = ({
  telemetryData,
}) => {
  const [selectedCategory, setSelectedCategory] = useState("atmosphere_info");

  const formatKey = (key: string): string => {
    // スネークケースをタイトルケースに変換する
    return key
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  const renderDetails = () => {
    const details = telemetryData
      ? telemetryData[selectedCategory as keyof VesselTelemetryType]
      : null;
    if (!details) return null;

    return (
      <div>
        {Object.entries(details).map(([key, value]) => {
          if (Array.isArray(value)) {
            return (
              <div key={key}>
                <strong>{formatKey(key)}:</strong>
                <ul>
                  {value.map((item, index) => (
                    <li key={index}>
                      {Object.entries(item).map(([subKey, subValue]) => (
                        <div key={subKey}>
                          {formatKey(subKey)}: {subValue as string}
                        </div>
                      ))}
                    </li>
                  ))}
                </ul>
              </div>
            );
          }
          return (
            <div key={key}>
              <strong>{formatKey(key)}:</strong> {JSON.stringify(value)}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="w-full h-full text-[0.8rem]">
      <div className="text-center bg-gray-600">
        <h2 className="font-bold ">Vessel Telemetry</h2>
      </div>
      {!telemetryData ? (
        <div className="flex items-center justify-center w-full h-[90%]">
        <div className="text-center">
          Preparing to get vessel telemetry.
        </div>
      </div>
      ) : (
        <div className="px-[1rem] py-[0.4rem]">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="w-full px-[1rem] shadow-md rounded-md bg-gray-700"
          >
            <option value="surface_info">Surface Info</option>
            <option value="orbit_info">Orbit Info</option>
            <option value="atmosphere_info">Atmosphere Info</option>
            <option value="delta_v_status">Delta-V Status</option>
          </select>
          <div className="px-[1rem]">{renderDetails()}</div>
        </div>
      )}
    </div>
  );
};

export default VesselTelemetryViewer;
