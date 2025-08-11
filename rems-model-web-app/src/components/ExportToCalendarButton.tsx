import { useState } from "react";
import apiClient from "../services/axios";
import { useAuth } from "../context/AuthProvider";

interface ExportToCalendarButtonProps {
  schedule: any[];
}

export default function ExportToCalendarButton({
  schedule,
}: ExportToCalendarButtonProps) {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const scheduleId = schedule[0]?.id;
      const scheduleBody = schedule[1];
      const response = await apiClient.post(
        `/schedules/${scheduleId}/export-calendar`,
        {
          calendar_id: "primary",
          schedule: schedule
          
        }
      );

      console.log("Exported successfully:", response.data);
      alert("Schedule exported to Google Calendar!");
    } catch (error) {
      console.error("Export failed:", error);
      alert("Failed to export schedule to calendar");
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={isExporting}
      className="px-4 py-3 bg-green-500 text-white rounded hover:bg-green-600 cursor-pointer disabled:bg-gray-400"
    >
      {isExporting ? "Exporting..." : "Export to Calendar"}
    </button>
  );
}
