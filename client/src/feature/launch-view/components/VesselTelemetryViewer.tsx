import React, { useState } from "react";
import { VesselTelemetryType } from "../../../types/vesselTelemetryType";

interface VesselTelemetryViewerProps {
  telemetryData?: VesselTelemetryType;
}

const VesselTelemetryViewer: React.FC<VesselTelemetryViewerProps> = ({
  telemetryData,
}) => {
  const [selectedCategory, setSelectedCategory] = useState("surface_info");
  if (!telemetryData) {
    return (
      <div className="h-full w-full flex justify-center items-center">
        Preparing to get vessel telemetry.
      </div>
    );
  }
  const renderDetails = () => {
    const details =
      telemetryData[selectedCategory as keyof VesselTelemetryType];
    if (!details) return null;

    return (
      <div>
        {Object.entries(details).map(([key, value]) => {
          if (Array.isArray(value)) {
            return (
              <div key={key}>
                <strong>{key}:</strong>
                <ul>
                  {value.map((item, index) => (
                    <li key={index}>
                      {Object.entries(item).map(([subKey, subValue]) => (
                        <div key={subKey}>
                          {subKey}: {subValue as string}
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
              <strong>{key}:</strong> {JSON.stringify(value)}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="h-full w-full">
      <select
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}
      >
        <option value="">Select a category</option>
        <option value="surface_info">Surface Info</option>
        <option value="orbit_info">Orbit Info</option>
        <option value="atmosphere_info">Atmosphere Info</option>
        <option value="delta_v_status">Delta-V Status</option>
      </select>
      <div>{renderDetails()}</div>
    </div>
  );
};

export default VesselTelemetryViewer;
