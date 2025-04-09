import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";
import ProductList from "./ProductList";
import Dashboard from "./Dashboard";

const App = () => (
  <Router>
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  </Router>
);

export default App;
