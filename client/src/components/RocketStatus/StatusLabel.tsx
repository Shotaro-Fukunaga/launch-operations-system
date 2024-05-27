import React from "react";

type Props = {
  status: number | undefined;
  customLabels?: { [key: number]: string };
};

const StatusLabel: React.FC<Props> = ({ status, customLabels }) => {
  const defaultLabels: { [key: number]: string } = {
    0: "WAIT",
    1: "GO",
    2: "ACTIVE",
    3: "CUTOFF",
    99: "UNCONNECTED",
  };

  const statusClasses: { [key: number]: string } = {
    0: "bg-gray-400",
    1: "bg-green-300",
    2: "bg-blue-300",
    3: "bg-red-300",
    99: "bg-gray-500",
  };

  const effectiveStatus = status === undefined ? 99 : status;
  const statusText =
    customLabels && customLabels[effectiveStatus]
      ? customLabels[effectiveStatus]
      : defaultLabels[effectiveStatus] || "Unknown";
  const statusClass = statusClasses[effectiveStatus] || "status-unknown";

  return (
    <div className="flex gap-[0.4rem]">
      <p>Status:</p>
      <span className={`rounded-sm px-[0.3rem] ${statusClass}`}>
        {statusText}
      </span>
    </div>
  );
};

export default StatusLabel;
