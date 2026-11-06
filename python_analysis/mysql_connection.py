import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

# 1. MYSQL DATABASE CONNECTION
project_path = Path(__file__).resolve().parent.parent
load_dotenv(project_path / ".env")

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

if not all([username, password, host, database]):
    raise ValueError("Database credentials are missing. Check the project .env file.")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    database=database,
)
engine = create_engine(connection_url)

try:
    # 2. LOAD CUSTOMERS DATASET
    customers_df = pd.read_sql("SELECT * FROM customers", engine)
    print("Data loaded successfully!")

    # 3. BASIC DATA EXPLORATION
    print("\nFIRST 5 RECORDS:")
    print(customers_df.head())
    print("\nDATASET SHAPE:")
    print(customers_df.shape)
    print("\nCOLUMN NAMES:")
    print(customers_df.columns)
    print("\nDATA TYPES:")
    print(customers_df.dtypes)

    # 4. DATA QUALITY CHECKS
    print("\nMISSING VALUES:")
    print(customers_df.isnull().sum())
    print("\nDUPLICATE RECORDS:")
    print(customers_df.duplicated().sum())
    print("\nSTATISTICAL SUMMARY:")
    print(customers_df.describe(include="all"))

    # 5. CUSTOMER ANALYSIS
    customer_counts = customers_df["customer_unique_id"].value_counts()
    repeat_customers = customer_counts[customer_counts > 1]
    print("\nTOTAL CUSTOMER RECORDS:")
    print(len(customers_df))
    print("\nUNIQUE CUSTOMERS:")
    print(customers_df["customer_unique_id"].nunique())
    print("\nCUSTOMERS WITH MULTIPLE RECORDS:")
    print(len(repeat_customers))

    # 6. TOP 10 CUSTOMER CITIES
    print("\nTOP 10 CUSTOMER CITIES:")
    print(customers_df["customer_city"].value_counts().head(10))

    # 7. TOP 10 CUSTOMER STATES
    print("\nTOP 10 CUSTOMER STATES:")
    print(customers_df["customer_state"].value_counts().head(10))
    print("\nCUSTOMER ANALYSIS COMPLETED SUCCESSFULLY!")
        # 8. LOAD ORDERS DATASET
    orders_df = pd.read_sql("SELECT * FROM orders", engine)
    print("\n========== ORDERS ANALYSIS ==========")
    print("\nFIRST 5 ORDERS:")
    print(orders_df.head())
    print("\nORDERS DATASET SHAPE:")
    print(orders_df.shape)
    print("\nORDERS COLUMNS:")
    print(orders_df.columns)
    print("\nORDERS DATA TYPES:")
    print(orders_df.dtypes)
    print("\nORDERS MISSING VALUES:")
    print(orders_df.isnull().sum())
    print("\nORDERS DUPLICATE RECORDS:")
    print(orders_df.duplicated().sum())
    print("\nORDER STATUS DISTRIBUTION:")
    print(orders_df["order_status"].value_counts())

    orders_df["order_purchase_timestamp"] = pd.to_datetime(
        orders_df["order_purchase_timestamp"], errors="coerce"
    )
    orders_df["purchase_year"] = orders_df["order_purchase_timestamp"].dt.year
    orders_df["purchase_month"] = orders_df["order_purchase_timestamp"].dt.month
    print("\nORDERS BY YEAR:")
    print(orders_df["purchase_year"].value_counts().sort_index())
    print("\nORDERS ANALYSIS COMPLETED!")

    # 9. ORDER DELIVERY PERFORMANCE
    print("\n========== DELIVERY PERFORMANCE ==========")
    date_columns = [
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for column in date_columns:
        orders_df[column] = pd.to_datetime(orders_df[column], errors="coerce")

    delivered_orders = orders_df[
        orders_df["order_status"] == "delivered"
    ].copy()
    delivered_orders["delivery_days"] = (
        delivered_orders["order_delivered_customer_date"]
        - delivered_orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    delivered_orders["delay_days"] = (
        delivered_orders["order_delivered_customer_date"]
        - delivered_orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    print("\nAVERAGE DELIVERY TIME (DAYS):")
    print(round(delivered_orders["delivery_days"].mean(), 2))
    late_orders = delivered_orders[delivered_orders["delay_days"] > 0]
    print("\nTOTAL LATE DELIVERIES:")
    print(len(late_orders))
    on_time_orders = delivered_orders[delivered_orders["delay_days"] <= 0]
    print("\nON-TIME OR EARLY DELIVERIES:")
    print(len(on_time_orders))
    total_deliveries = len(delivered_orders)
    if total_deliveries > 0:
    
        on_time_percentage = len(on_time_orders) / total_deliveries * 100
        print("\nON-TIME DELIVERY PERCENTAGE:")
        print(round(on_time_percentage, 2), "%")
    print("\nDELIVERY PERFORMANCE ANALYSIS COMPLETED!")

    # 10. PRODUCT SALES ANALYSIS
    print("\n========== PRODUCT SALES ANALYSIS ==========")
    order_items_df = pd.read_sql("SELECT * FROM order_items", engine)
    products_df = pd.read_sql("SELECT * FROM products", engine)
    sales_df = pd.merge(order_items_df, products_df, on="product_id", how="left")
    print("\nTOTAL UNITS SOLD:")
    print(len(sales_df))
    total_revenue = sales_df["price"].sum()
    print("\nTOTAL PRODUCT REVENUE:")
    print(round(total_revenue, 2))
    print("\nAVERAGE PRODUCT PRICE:")
    print(round(sales_df["price"].mean(), 2))
    print("\nTOP 10 BEST-SELLING PRODUCTS:")
    top_products = (
        sales_df.groupby("product_id")
        .agg(
            units_sold=("order_item_id", "count"),
            revenue=("price", "sum"),
        )
        .sort_values("units_sold", ascending=False)
        .head(10)
    )
    print(top_products)

    # 11. PRODUCT CATEGORY ANALYSIS
    category_df = pd.read_sql("SELECT * FROM category_translation", engine)
    sales_df = pd.merge(
        sales_df, category_df, on="product_category_name", how="left"
    )
    print("\nTOP 10 REVENUE-GENERATING CATEGORIES:")
    category_revenue = (
        sales_df.groupby("product_category_name_english")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print(category_revenue)
    print("\nPRODUCT SALES ANALYSIS COMPLETED!")

    # 12. PAYMENT ANALYSIS
    print("\n========== PAYMENT ANALYSIS ==========")
    payments_df = pd.read_sql("SELECT * FROM order_payments", engine)
    print("\nPAYMENT DATASET SHAPE:")
    print(payments_df.shape)
    print("\nPAYMENT DATA TYPES:")
    print(payments_df.dtypes)
    print("\nMISSING VALUES:")
    print(payments_df.isnull().sum())
    total_payment = payments_df["payment_value"].sum()
    print("\nTOTAL PAYMENT VALUE:")
    print(round(total_payment, 2))
    print("\nAVERAGE PAYMENT VALUE:")
    print(round(payments_df["payment_value"].mean(), 2))
    print("\nPAYMENT METHOD DISTRIBUTION:")
    print(payments_df["payment_type"].value_counts())
    print("\nPAYMENT VALUE BY PAYMENT METHOD:")
    payment_revenue = (
        payments_df.groupby("payment_type")["payment_value"]
        .sum()
        .sort_values(ascending=False)
    )
    print(payment_revenue.round(2))
    print("\nAVERAGE PAYMENT INSTALMENTS:")
    print(round(payments_df["payment_installments"].mean(), 2))
    print("\nPAYMENT METHOD PERCENTAGES:")
    print((payments_df["payment_type"].value_counts(normalize=True) * 100).round(2))
    print("\nPAYMENT ANALYSIS COMPLETED!")

    # 13. CUSTOMER REVIEW ANALYSIS
    print("\n========== CUSTOMER REVIEW ANALYSIS ==========")
    reviews_df = pd.read_sql("SELECT * FROM order_reviews", engine)
    print("\nREVIEW DATASET SHAPE:")
    print(reviews_df.shape)
    print("\nMISSING VALUES:")
    print(reviews_df.isnull().sum())
    print("\nAVERAGE REVIEW SCORE:")
    print(round(reviews_df["review_score"].mean(), 2))
    print("\nREVIEW SCORE DISTRIBUTION:")
    print(reviews_df["review_score"].value_counts().sort_index())
    print("\nREVIEW SCORE PERCENTAGES:")
    print(
        (reviews_df["review_score"].value_counts(normalize=True).sort_index() * 100).round(2)
    )
    positive_reviews = reviews_df[reviews_df["review_score"] >= 4]
    print("\nPOSITIVE REVIEWS:")
    print(len(positive_reviews))
    negative_reviews = reviews_df[reviews_df["review_score"] <= 2]
    print("\nNEGATIVE REVIEWS:")
    print(len(negative_reviews))
    print("\nMISSING REVIEW COMMENTS:")
    print(reviews_df["review_comment_message"].isnull().sum())
    print("\nCUSTOMER REVIEW ANALYSIS COMPLETED!")

    # 14. EXPORT DATASETS FOR POWER BI
    print("\n========== EXPORTING DATASETS ==========")
    output_folder = project_path / "data" / "processed"
    output_folder.mkdir(parents=True, exist_ok=True)
    sellers_df = pd.read_sql("SELECT * FROM sellers", engine)

    datasets = {
        "customers.csv": customers_df,
        "orders.csv": orders_df,
        "order_items.csv": order_items_df,
        "products.csv": products_df,
        "payments.csv": payments_df,
        "reviews.csv": reviews_df,
        "sellers.csv": sellers_df,
        "category_translation.csv": category_df,
        "sales_details.csv": sales_df,
    }

    for filename, dataframe in datasets.items():
        file_path = output_folder / filename
        dataframe.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"{filename} exported successfully | Rows: {len(dataframe)}")

    print("\nALL DATASETS EXPORTED SUCCESSFULLY!")

except Exception as e:
    print("Error:", e)

finally:
    engine.dispose()
