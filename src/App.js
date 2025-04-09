import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";
import Recommendations from "./components/Recommendations";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/recommendations/:productId" element={<Recommendations />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
