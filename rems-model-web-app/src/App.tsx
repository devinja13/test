import { useState } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import UploadContainer from "./components/UploadContainer";
import GeneratedSchedule from "./components/GeneratedSchedule";
import Navbar from "./components/Navbar";
import NotFoundPage from "./components/NotFoundPage";


// router navigation object
const router = createBrowserRouter([
  {
    path: "/",
    element: <UploadContainer />,
    errorElement: <NotFoundPage />,
  },
  {
    path: "/view-schedule",
    element: <GeneratedSchedule />,
    errorElement: <NotFoundPage />,
  },
]);

function App() {
  // flex items-center justify-center
  return (
    <div className="min-h-screen  bg-stone-200">
      <Navbar />
      <div className="pt-15 ">
        <RouterProvider router={router} />
        {/* <UploadContainer /> */}
      </div>
    </div>
  );
}

export default App;
