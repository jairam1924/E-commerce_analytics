import { Link } from "react-router-dom";

const ProductCard = ({ product }) => (
  <div className="bg-white shadow-md p-4 rounded-xl">
    <h2 className="text-lg font-semibold">{product.product_name}</h2>
    <p>₹{product.discounted_price}</p>
    <p>Category: {product.category}</p>
    <Link to={`/recommendations/${product.product_id}`} className="text-blue-500">
      View Recommendations →
    </Link>
  </div>
);

export default ProductCard;
