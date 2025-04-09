import React, { useEffect, useState } from "react";
import axios from "axios";

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/products")
      .then(res => {
        setProducts(res.data);
        setFiltered(res.data);
        const cats = [...new Set(res.data.map(p => p.category))];
        setCategories(cats);
      })
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    let results = products;

    if (selectedCategory) {
      results = results.filter(p => p.category === selectedCategory);
    }

    if (searchTerm) {
      results = results.filter(p =>
        p.product_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFiltered(results);
  }, [searchTerm, selectedCategory, products]);

  return (
    <div className="p-6">
      {/* <h1 className="text-3xl font-bold mb-6 text-center">🛒 Ecom Analytics</h1> */}

      {/* Search + Filter */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
        <input
          type="text"
          placeholder="Search products..."
          className="border p-2 rounded w-full sm:w-1/2"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <select
          className="border p-2 rounded w-full sm:w-1/4"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      {/* Product Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filtered.map(product => (
            <div key={product.product_id} className="border rounded-2xl shadow p-4 hover:shadow-lg transition">
              <h2 className="text-lg font-semibold mb-1">{product.product_name}</h2>
              <p className="text-sm text-gray-600">Category: {product.category}</p>
              <p className="text-sm text-gray-600">Price: ₹{product.discounted_price}</p>
              <p className="text-sm text-yellow-500">⭐ {product.rating || "No rating"}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center text-gray-500">No products found.</div>
      )}
    </div>
  );
};

export default ProductList;
