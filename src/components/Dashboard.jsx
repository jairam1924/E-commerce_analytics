import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#00C49F', '#FFBB28', '#A28CF1', '#00B8D9'];

const Dashboard = () => {
  const [salesData, setSalesData] = useState([]);
  const [inventoryData, setInventoryData] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/sales')
      .then(res => setSalesData(res.data))
      .catch(err => console.error('Sales API error:', err));

    axios.get('http://127.0.0.1:5000/api/inventory')
      .then(res => {
        const cleaned = res.data.map(item => ({
          ...item,
          subcategory: item.category.split('|').pop().replace(/([a-z])([A-Z])/g, '$1 $2').replace(/&/g, ' & ')
        }));
        setInventoryData(cleaned);
      })
      .catch(err => console.error('Inventory API error:', err));
  }, []);

  return (
    <div className="p-4 space-y-8">

      {/* Inventory Pie Chart */}
      <div className="bg-white p-4 rounded-2xl shadow-md">
        <h2 className="text-2xl font-semibold mb-4 text-green-600">📦 Inventory Breakdown (Visual)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={inventoryData}
              dataKey="count"
              nameKey="subcategory"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
            >
              {inventoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Inventory Cards */}
      <div>
        <h2 className="text-2xl font-semibold mb-4 text-gray-700">🗂️ Inventory Details</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {inventoryData.map((item, idx) => (
            <div key={idx} className="bg-white shadow rounded-xl p-4">
              <h3 className="text-lg font-semibold">{item.subcategory}</h3>
              <p className="text-sm text-gray-500 truncate">{item.category}</p>
              <p className="text-xl font-bold">{item.count} items</p>
            </div>
          ))}
        </div>
      </div>

      {/* Sales Chart */}
      <div>
        <h2 className="text-2xl font-semibold mb-4 text-blue-600">📊 Sales Overview</h2>
        <div className="bg-white p-4 rounded-2xl shadow-md">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salesData}>
              {/* <XAxis dataKey="subcategory" /> */}
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total_revenue" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
