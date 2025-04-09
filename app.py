from flask import Flask, jsonify, request
import mysql.connector
import mysql
from flask_cors import CORS
import re


app = Flask(__name__)
CORS(app, origins="http://localhost:3000")
# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="JaiRam2219",
    database="ecom_analytics"
)
def get_db_cursor():
    global db
    if not db.is_connected():
        db.reconnect()
    return db.cursor(dictionary=True)
cursor = get_db_cursor()

# # 1️⃣ Fetch All Sales Data
# @app.route('/products', methods=['GET'])
# def get_filtered_products():
#     # Get query params
#     category = request.args.get('category', None)
#     min_price = request.args.get('min_price', 0, type=float)
#     max_price = request.args.get('max_price', 999999, type=float)
#     sort_by = request.args.get('sort_by', 'discounted_price')  # Sort by price/rating
#     order = request.args.get('order', 'asc')  # asc / desc
#     limit = request.args.get('limit', 10, type=int)
#     offset = request.args.get('offset', 0, type=int)

#     # Build SQL Query
#     query = "SELECT * FROM sales_data WHERE discounted_price BETWEEN %s AND %s"
#     params = [min_price, max_price]

#     if category:
#         query += " AND category = %s"
#         params.append(category)

#     query += f" ORDER BY {sort_by} {order.upper()} LIMIT %s OFFSET %s"
#     params.extend([limit, offset])

#     cursor.execute(query, params)
#     products = cursor.fetchall()
#     return jsonify(products)

@app.route("/top-products")
def top_products():
    try:
        cursor.execute("SELECT * FROM sales_data ORDER BY rating DESC, rating_count DESC LIMIT 10;")
        top_products = cursor.fetchall()
        return jsonify(top_products)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')

    query = "SELECT product_id, product_name, discounted_price, category FROM sales_data"
    if category:
        query += " WHERE category = %s"
        cursor.execute(query, (category,))
    else:
        cursor.execute(query)

    results = cursor.fetchall()
    return jsonify(results)
    # cursor = db.cursor(dictionary=True)

    # # Get query parameters
    # category = request.args.get("category", "").strip().lower()
    # min_price = request.args.get("min_price", type=float)
    # max_price = request.args.get("max_price", type=float)
    # min_rating = request.args.get("min_rating", type=float)
    # sort_by = request.args.get("sort_by", "").strip().lower()
    # search_query = request.args.get("search", "").strip().lower()  # New search query param
    # page = request.args.get("page", type=int, default=1)
    # limit = request.args.get("limit", type=int, default=10)

    # # Calculate offset
    # offset = (page - 1) * limit

    # # Base SQL query
    # query = "SELECT * FROM sales_data WHERE 1=1"
    # params = []

    # # Apply filters
    # if category:
    #     query += " AND LOWER(category) = %s"
    #     params.append(category)
    # if min_price is not None:
    #     query += " AND discounted_price >= %s"
    #     params.append(min_price)
    # if max_price is not None:
    #     query += " AND discounted_price <= %s"
    #     params.append(max_price)
    # if min_rating is not None:
    #     query += " AND rating >= %s"
    #     params.append(min_rating)

    # # Search feature
    # if search_query:
    #     query += " AND (LOWER(product_name) LIKE %s OR LOWER(category) LIKE %s OR LOWER(about_product) LIKE %s)"
    #     search_term = f"%{search_query}%"
    #     params.extend([search_term, search_term, search_term])

    # # Sorting options
    # if sort_by in ["discounted_price", "rating"]:
    #     query += f" ORDER BY {sort_by} ASC"

    # # Apply pagination
    # query += " LIMIT %s OFFSET %s"
    # params.extend([limit, offset])

    # # Execute the query
    # cursor.execute(query, tuple(params))
    # products = cursor.fetchall()

    # # Get total product count
    # count_query = "SELECT COUNT(*) as total FROM sales_data WHERE 1=1"
    # cursor.execute(count_query)
    # total_count = cursor.fetchone()["total"]

    # # Return paginated response
    # return jsonify({
    #     "total_products": total_count,
    #     "page": page,
    #     "limit": limit,
    #     "total_pages": (total_count // limit) + (1 if total_count % limit else 0),
    #     "data": products
    # })
    
@app.route('/api/sales')
def revenue_data():
    cursor = get_db_cursor()
    cursor.execute("""
        SELECT DATE(collected_at ) as date, SUM(discounted_price) as total_revenue
        FROM sales_data
        GROUP BY DATE(collected_at )
        ORDER BY DATE(collected_at )
    """)
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/inventory')
def inventory_data():
    cursor = get_db_cursor()
    cursor.execute("SELECT category, COUNT(*) as count FROM sales_data GROUP BY category")
    data = cursor.fetchall()

    cleaned_data = []
    for item in data:
        full_path = item['category']
        parts = full_path.split('|')
        subcategory = parts[-1] if parts else 'Unknown'

        # Clean subcategory: replace "&", camelCase to spaces
        clean_sub = re.sub(r'([a-z])([A-Z])', r'\1 \2', subcategory)
        clean_sub = clean_sub.replace('&', ' and ')

        cleaned_data.append({
            "category": full_path,
            "subcategory": clean_sub,
            "count": item['count']
        })

    return jsonify(cleaned_data)


@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    cursor = get_db_cursor()

    # Get product_id from request
    product_id = request.args.get("product_id", "").strip()
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    # Fetch details of the given product
    cursor.execute("SELECT category, discounted_price FROM sales_data WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    category = product["category"]
    price = product["discounted_price"]

    # Find similar products in the same category and similar price range
    query = """
        SELECT * FROM sales_data
        WHERE category = %s AND discounted_price BETWEEN %s AND %s AND product_id != %s
        ORDER BY RAND() LIMIT 5
    """
    price = float(price)  # Convert Decimal to float
    price_range = (price * 0.8, price * 1.2)
    cursor.execute(query, (category, price_range[0], price_range[1], product_id))
    recommendations = cursor.fetchall()

    return jsonify({"product_id": product_id, "recommended_products": recommendations})

# 2️⃣ Fetch Product by ID
@app.route('/products/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    cursor.execute("SELECT * FROM sales_data WHERE product_id = %s;", (product_id,))
    product = cursor.fetchone()
    return jsonify(product) if product else jsonify({"error": "Product not found"}), 404

# 3️⃣ Get Top-Selling Products (Highest Rating)
# @app.route('/top-products', methods=['GET'])
# def get_top_products():
#     cursor.execute("SELECT * FROM sales_data ORDER BY rating DESC, rating_count DESC LIMIT 10;")
#     top_products = cursor.fetchall()
#     return jsonify(top_products)

# 4️⃣ Get Average Rating per Category
@app.route('/avg-rating', methods=['GET'])
def get_avg_rating():
    cursor.execute("SELECT category, AVG(rating) AS avg_rating FROM sales_data GROUP BY category;")
    avg_ratings = cursor.fetchall()
    return jsonify(avg_ratings)

if __name__ == '__main__':
    app.run(debug=True)
