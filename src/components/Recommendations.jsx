import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

const Recommendations = () => {
  const { productId } = useParams();
  const [recommended, setRecommended] = useState([]);

  useEffect(() => {
    axios.get(`http://127.0.0.1:5000/recommendations?product_id=${productId}`)
      .then(res => setRecommended(res.data))
      .catch(err => console.error(err));
  }, [productId]);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Recommended Products</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {recommended.map(prod => (
          <div key={prod.product_id} className="bg-white p-4 shadow-md rounded-xl">
            <h3 className="font-semibold">{prod.product_name}</h3>
            <p>₹{prod.discounted_price}</p>
            <p>Rating: {prod.rating}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;
