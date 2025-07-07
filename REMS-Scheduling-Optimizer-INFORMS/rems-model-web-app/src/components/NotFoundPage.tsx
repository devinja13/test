import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="mt-5 mx-0 my-auto">
      <div className="text-center">
        <h1>404 Not Found</h1>
        <Link to="/">Home Page</Link>
      </div>
    </div>
  );
}
