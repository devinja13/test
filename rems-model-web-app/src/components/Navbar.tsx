import { useState } from "react";

export default function Navbar() {
  const [isSignedIn, setIsSignedIn] = useState<Boolean>(false);
  return (
    <header className="sticky top-0 left-0 right-0 z-40 shadow-sm bg-white p-5">
      <nav className="flex justify-between w-full">
        {/* Organization */}
        <div className="ml-20">
          <h3>Rice EMS</h3>
        </div>
        {/* Sign In / Out button */}
        <button className="mr-20">{`Sign ${isSignedIn ? "Out" : "In"}`}</button>
      </nav>
    </header>
  );
}
