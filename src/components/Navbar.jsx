import { Link } from "react-router-dom";

const Navbar = () => (
  <nav className="bg-blue-600 text-white p-4 flex justify-between items-center">
    <h1 className="text-xl font-bold">🛒 Ecom Analytics</h1>
    <div className="space-x-4">
      <Link to="/" className="hover:underline">Home</Link>
      <Link to="/dashboard" className="hover:underline">Dashboard</Link>
    </div>
  </nav>
);

export default Navbar;
