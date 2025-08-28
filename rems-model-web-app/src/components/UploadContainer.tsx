// UploadContainer.tsx
// BEFORE:
// import { use, useEffect, useState } from "react";
// AFTER:
import { useEffect, useState } from "react";

import { useNavigate } from "react-router";
import apiClient from "../services/axios";
import useDrivePicker from "react-google-drive-picker";
import { Stepper } from "react-form-stepper";
import { FaGoogleDrive } from "react-icons/fa6";
import { useAuth } from "../context/AuthProvider";

// Prefer primitive string
type SpreadsheetData = {
  fileId: string | undefined;
};

export default function UploadContainer() {
  const [openPicker, authResponse] = useDrivePicker();
  const [currentFileId, setCurrentFileId] = useState<string | undefined>();
  const { token, setGoogleToken } = useAuth(); // if token is unused, prefix with _token to silence TS
  const api = apiClient;
  const navigate = useNavigate();

  useEffect(() => {
    if (authResponse?.access_token) {
      setGoogleToken(authResponse.access_token);
    }
  }, [authResponse, setGoogleToken]);

  useEffect(() => {
    const sendSpreadsheetData = async () => {
      if (!currentFileId) return;

      const spreadsheetData: SpreadsheetData = { fileId: currentFileId };
      const response = await api.post("/schedules", spreadsheetData);

      const schedule = response.data.schedule;
      navigate("/view-schedule", { state: { schedule } });
    };

    if (currentFileId) sendSpreadsheetData();
  }, [currentFileId, navigate, api]);

  // ✅ Complete style config that matches StepStyleDTO
  const stepperStyles = {
    activeBgColor: "#064e3b",
    activeTextColor: "#ffffff",
    completedBgColor: "#9ca3af",
    completedTextColor: "#ffffff",
    inactiveBgColor: "#9ca3af",
    inactiveTextColor: "#ffffff",
    size: "2em",
    circleFontSize: "1rem",
    labelFontSize: "0.875rem",
    borderRadius: "50%",
    fontWeight: 500
  };

  const handleOpenPicker = () => {
    openPicker({
      clientId: import.meta.env.VITE_CLIENT_ID as string,
      developerKey: import.meta.env.VITE_DEVELOPER_KEY as string,
      customScopes: [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/calendar",
      ],
      showUploadView: true,
      showUploadFolders: true,
      supportDrives: true,
      multiselect: false,
      callbackFunction: (data) => {
        if (data.action === "picked" && data.docs?.length) {
          const pickedFileId = data.docs[0]["id"] as string;
          setCurrentFileId(() => pickedFileId);
        }
      },
    });
  };

  return (
    <div className="max-w-3xl md: max-w mx-auto px-4 sm:px-6 lg:px-24 mt-16 bg-white rounded-lg shadow-md py-12 flex flex-col justify-between gap-4">
      <h2 className="text-3xl font-bold">Automated Shift Scheduler</h2>
      <p className="text-xl ">
        Upload your CSV google form responses, and we'll generate an optimized schedule for next month.
      </p>

      <Stepper
        steps={[
          { label: "Sign in with OAuth" },
          { label: "Upload CSV" },
          { label: "View Generated Schedule" },
        ]}
        activeStep={1}
        styleConfig={stepperStyles}   // ✅ use the full config
      />

      <div
        onClick={handleOpenPicker}
        className="px-5 py-2.5 border-dotted border-2 border-gray-500 rounded-sm w-full min-h-[200px] flex items-center justify-center"
      >
        <button className="w-5/12 flex flex-col gap-4">
          <FaGoogleDrive className="mx-auto my-auto text-xl" />
          <p>Import from Google Drive</p>
        </button>
      </div>
    </div>
  );
}
