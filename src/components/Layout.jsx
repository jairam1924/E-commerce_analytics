import Navbar from './Navbar';

const Layout = ({ children }) => (
  <div className="flex h-screen bg-gray-100">
    <aside className="w-64 bg-blue-700 text-white p-4">
      <h2 className="text-2xl font-bold mb-4">📊 Dashboard</h2>
      <ul>
        <li className="my-2"><a href="/" className="hover:underline">Products</a></li>
        <li className="my-2"><a href="/dashboard" className="hover:underline">Analytics</a></li>
      </ul>
    </aside>
    <main className="flex-1 p-6 overflow-y-auto">
      <Navbar />
      {children}
    </main>
  </div>
);

export default Layout;
