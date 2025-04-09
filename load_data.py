import pandas as pd
import mysql.connector
import re
import numpy as np


# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",      # Change this if your MySQL username is different
    password="JaiRam2219",  # Change this to your MySQL password
    database="ecom_analytics"
)
cursor = db.cursor()

# Load CSV
df = pd.read_csv("amazon.csv", encoding="utf-8", sep=",", low_memory=False)
# df.to_csv("debug_output.csv", index=False)


# print(df[df.applymap(lambda x: str(x).lower() == "nan")])

# print(df.head())  # Ensure 'nan' is not in the data
# print(df.dtypes)  # Verify correct data types

  # Convert NaN to None

# print(df["product_name"].astype(str).apply(len).max())

def clean_rating(value):
    if pd.isna(value):  # Handle NaN values
        return None  # Store as NULL in MySQL
    
    if isinstance(value, str):  # Ensure it's a string before replacing
        value = re.sub(r"[^\d.]", "", value)  # Remove non-numeric characters
        return float(value) if value else None  # Convert to float
    
    return float(value)  # If it's already a number, return as is



# Function to clean numeric values
def clean_numeric(value):
    if pd.isna(value):  # Handle NaN values
        return 0 # Default value for missing data
    
    value=str(value).encode('utf-8').decode('utf-8')
    value = re.sub(r"[^\d.]", "", value)  # Remove ₹, %, commas, etc.
    return float(value) if value else 0 # Convert to integer
    

# Apply cleaning function
df["rating"] = df["rating"].apply(clean_rating)
df["discounted_price"] = df["discounted_price"].apply(clean_numeric)
df["actual_price"] = df["actual_price"].apply(clean_numeric)
df["discount_percentage"] = df["discount_percentage"].apply(clean_numeric)
df["rating_count"] = df["rating_count"].apply(clean_numeric) 


df["discounted_price"] = pd.to_numeric(df["discounted_price"], errors="coerce").fillna(0)
df["actual_price"] = pd.to_numeric(df["actual_price"], errors="coerce").fillna(0)
df["discount_percentage"] = pd.to_numeric(df["discount_percentage"], errors="coerce").fillna(0)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce").fillna(0)

print(df[['discounted_price']].head(10))
df = df.drop_duplicates(subset=["product_id"], keep="last")

# Define SQL Insert Query
insert_query = """
    INSERT INTO sales_data (
        product_id, product_name, category, discounted_price, actual_price,
        discount_percentage, rating, rating_count, about_product,
        user_id, user_name, review_id, review_title, review_content,
        img_link, product_link, source, collected_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())

    ON DUPLICATE KEY UPDATE 
    discounted_price = VALUES(discounted_price), 
    actual_price = VALUES(actual_price), 
    discount_percentage = VALUES(discount_percentage), 
    rating = VALUES(rating), 
    rating_count = VALUES(rating_count), 
    about_product = VALUES(about_product), 
    review_title = VALUES(review_title), 
    review_content = VALUES(review_content);
"""


# Insert Data into MySQL
for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row["product_id"], row["product_name"], row["category"],
        row["discounted_price"], row["actual_price"], row["discount_percentage"],
        row["rating"], row["rating_count"], row["about_product"],
        row["user_id"], row["user_name"], row["review_id"],
        row["review_title"], row["review_content"],
        row["img_link"], row["product_link"], "Public Dataset"
    ))

db.commit()
cursor.close()
db.close()

print("✅ Data successfully loaded into MySQL!")
