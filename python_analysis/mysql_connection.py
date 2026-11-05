
import pandas as pd
from sqlalchemy import create_engine, URL

# ==================================
# 1. MYSQL DATABASE CONNECTION
# ==================================

username = "root"
password = "Bhavya@2006"
host = "localhost"
database = "ecommerce_analytics"

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=host,
    database=database
)

engine = create_engine(connection_url)

try:
    # ==================================
    # 2. LOAD CUSTOMERS DATASET
    # ==================================

    customers_df = pd.read_sql(
        "SELECT * FROM customers",
        engine
    )

    print("Data loaded successfully!")

    # ==================================
    # 3. BASIC DATA EXPLORATION
    # ==================================

    print("\nFIRST 5 RECORDS:")
    print(customers_df.head())

    print("\nDATASET SHAPE:")
    print(customers_df.shape)

    print("\nCOLUMN NAMES:")
    print(customers_df.columns)

    print("\nDATA TYPES:")
    print(customers_df.dtypes)

    # ==================================
    # 4. DATA QUALITY CHECKS
    # ==================================

    print("\nMISSING VALUES:")
    print(customers_df.isnull().sum())

    print("\nDUPLICATE RECORDS:")
    print(customers_df.duplicated().sum())

    print("\nSTATISTICAL SUMMARY:")
    print(customers_df.describe(include="all"))

    # ==================================
    # 5. CUSTOMER ANALYSIS
    # ==================================

    customer_counts = customers_df[
        "customer_unique_id"
    ].value_counts()

    repeat_customers = customer_counts[
        customer_counts > 1
    ]

    print("\nTOTAL CUSTOMER RECORDS:")
    print(len(customers_df))

    print("\nUNIQUE CUSTOMERS:")
    print(customers_df["customer_unique_id"].nunique())

    print("\nCUSTOMERS WITH MULTIPLE RECORDS:")
    print(len(repeat_customers))

    # ==================================
    # 6. TOP 10 CUSTOMER CITIES
    # ==================================

    print("\nTOP 10 CUSTOMER CITIES:")
    print(
        customers_df["customer_city"]
        .value_counts()
        .head(10)
    )

    # ==================================
    # 7. TOP 10 CUSTOMER STATES
    # ==================================

    print("\nTOP 10 CUSTOMER STATES:")
    print(
        customers_df["customer_state"]
        .value_counts()
        .head(10)
    )

    print("\nCUSTOMER ANALYSIS COMPLETED SUCCESSFULLY!")
    
        # ==================================
    # 8. LOAD ORDERS DATASET
    # ==================================

    orders_df = pd.read_sql(
        "SELECT * FROM orders",
        engine
    )

    print("\n========== ORDERS ANALYSIS ==========")

    # First 5 records
    print("\nFIRST 5 ORDERS:")
    print(orders_df.head())

    # Dataset shape
    print("\nORDERS DATASET SHAPE:")
    print(orders_df.shape)

    # Column names
    print("\nORDERS COLUMNS:")
    print(orders_df.columns)

    # Data types
    print("\nORDERS DATA TYPES:")
    print(orders_df.dtypes)

    # Missing values
    print("\nORDERS MISSING VALUES:")
    print(orders_df.isnull().sum())

    # Duplicate records
    print("\nORDERS DUPLICATE RECORDS:")
    print(orders_df.duplicated().sum())

    # Order status distribution
    print("\nORDER STATUS DISTRIBUTION:")
    print(orders_df["order_status"].value_counts())

    # Convert purchase timestamp to datetime
    orders_df["order_purchase_timestamp"] = pd.to_datetime(
        orders_df["order_purchase_timestamp"]
    )

    # Extract purchase year and month
    orders_df["purchase_year"] = (
        orders_df["order_purchase_timestamp"].dt.year
    )

    orders_df["purchase_month"] = (
        orders_df["order_purchase_timestamp"].dt.month
    )

    print("\nORDERS BY YEAR:")
    print(orders_df["purchase_year"].value_counts().sort_index())

    print("\nORDERS ANALYSIS COMPLETED!")
    
        # ==================================
    # 9. ORDER DELIVERY PERFORMANCE
    # ==================================

    print("\n========== DELIVERY PERFORMANCE ==========")

    # Convert delivery dates into datetime format
    date_columns = [
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        orders_df[column] = pd.to_datetime(
            orders_df[column],
            errors="coerce"
        )

    # Select only delivered orders
    delivered_orders = orders_df[
        orders_df["order_status"] == "delivered"
    ].copy()

    # Calculate actual delivery time in days
    delivered_orders["delivery_days"] = (
        delivered_orders["order_delivered_customer_date"]
        - delivered_orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    # Calculate delivery delay in days
    delivered_orders["delay_days"] = (
        delivered_orders["order_delivered_customer_date"]
        - delivered_orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    # Average delivery time
    print("\nAVERAGE DELIVERY TIME (DAYS):")
    print(round(delivered_orders["delivery_days"].mean(), 2))

    # Late deliveries
    late_orders = delivered_orders[
        delivered_orders["delay_days"] > 0
    ]

    print("\nTOTAL LATE DELIVERIES:")
    print(len(late_orders))

    # On-time or early deliveries
    on_time_orders = delivered_orders[
        delivered_orders["delay_days"] <= 0
    ]

    print("\nON-TIME OR EARLY DELIVERIES:")
    print(len(on_time_orders))

    # Delivery performance percentage
    total_deliveries = len(delivered_orders)

    if total_deliveries > 0:
        on_time_percentage = (
            len(on_time_orders) / total_deliveries
        ) * 100

        print("\nON-TIME DELIVERY PERCENTAGE:")
        print(round(on_time_percentage, 2), "%")

    print("\nDELIVERY PERFORMANCE ANALYSIS COMPLETED!")
    
        # ==================================
    # 10. PRODUCT SALES ANALYSIS
    # ==================================

    print("\n========== PRODUCT SALES ANALYSIS ==========")

    # Load order items
    order_items_df = pd.read_sql(
        "SELECT * FROM order_items",
        engine
    )

    # Load products
    products_df = pd.read_sql(
        "SELECT * FROM products",
        engine
    )

    # Merge order items and products
    sales_df = pd.merge(
        order_items_df,
        products_df,
        on="product_id",
        how="left"
    )

    # Total units sold
    print("\nTOTAL UNITS SOLD:")
    print(len(sales_df))

    # Total product revenue
    total_revenue = sales_df["price"].sum()

    print("\nTOTAL PRODUCT REVENUE:")
    print(round(total_revenue, 2))

    # Average product price
    print("\nAVERAGE PRODUCT PRICE:")
    print(round(sales_df["price"].mean(), 2))

    # Top 10 best-selling products
    print("\nTOP 10 BEST-SELLING PRODUCTS:")

    top_products = (
        sales_df.groupby("product_id")
        .agg(
            units_sold=("order_item_id", "count"),
            revenue=("price", "sum")
        )
        .sort_values("units_sold", ascending=False)
        .head(10)
    )

    print(top_products)

    # ==================================
    # 11. PRODUCT CATEGORY ANALYSIS
    # ==================================

    category_df = pd.read_sql(
        "SELECT * FROM category_translation",
        engine
    )

    sales_df = pd.merge(
        sales_df,
        category_df,
        on="product_category_name",
        how="left"
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
    
        # ==================================
    # 12. PAYMENT ANALYSIS
    # ==================================

    print("\n========== PAYMENT ANALYSIS ==========")

    # Load payment dataset
    payments_df = pd.read_sql(
        "SELECT * FROM order_payments",
        engine
    )

    # Dataset overview
    print("\nPAYMENT DATASET SHAPE:")
    print(payments_df.shape)

    print("\nPAYMENT DATA TYPES:")
    print(payments_df.dtypes)

    print("\nMISSING VALUES:")
    print(payments_df.isnull().sum())

    # Total payment value
    total_payment = payments_df["payment_value"].sum()

    print("\nTOTAL PAYMENT VALUE:")
    print(round(total_payment, 2))

    # Average payment
    print("\nAVERAGE PAYMENT VALUE:")
    print(round(payments_df["payment_value"].mean(), 2))

    # Payment method distribution
    print("\nPAYMENT METHOD DISTRIBUTION:")
    print(payments_df["payment_type"].value_counts())

    # Revenue by payment method
    print("\nPAYMENT VALUE BY PAYMENT METHOD:")

    payment_revenue = (
        payments_df.groupby("payment_type")["payment_value"]
        .sum()
        .sort_values(ascending=False)
    )

    print(payment_revenue.round(2))

    # Average instalments
    print("\nAVERAGE PAYMENT INSTALMENTS:")
    print(round(payments_df["payment_installments"].mean(), 2))

    # Payment method percentages
    print("\nPAYMENT METHOD PERCENTAGES:")

    print(
        (
            payments_df["payment_type"]
            .value_counts(normalize=True) * 100
        ).round(2)
    )

    print("\nPAYMENT ANALYSIS COMPLETED!")
    
        # ==================================
    # 13. CUSTOMER REVIEW ANALYSIS
    # ==================================

    print("\n========== CUSTOMER REVIEW ANALYSIS ==========")

    # Load review dataset
    reviews_df = pd.read_sql(
        "SELECT * FROM order_reviews",
        engine
    )

    # Dataset shape
    print("\nREVIEW DATASET SHAPE:")
    print(reviews_df.shape)

    # Missing values
    print("\nMISSING VALUES:")
    print(reviews_df.isnull().sum())

    # Average review score
    print("\nAVERAGE REVIEW SCORE:")
    print(round(reviews_df["review_score"].mean(), 2))

    # Review score distribution
    print("\nREVIEW SCORE DISTRIBUTION:")
    print(reviews_df["review_score"].value_counts().sort_index())

    # Review score percentages
    print("\nREVIEW SCORE PERCENTAGES:")
    print(
        (reviews_df["review_score"].value_counts(
            normalize=True
        ).sort_index() * 100).round(2)
    )

    # Positive reviews (scores 4 and 5)
    positive_reviews = reviews_df[
        reviews_df["review_score"] >= 4
    ]

    print("\nPOSITIVE REVIEWS:")
    print(len(positive_reviews))

    # Negative reviews (scores 1 and 2)
    negative_reviews = reviews_df[
        reviews_df["review_score"] <= 2
    ]

    print("\nNEGATIVE REVIEWS:")
    print(len(negative_reviews))

    # Missing review comments
    print("\nMISSING REVIEW COMMENTS:")
    print(reviews_df["review_comment_message"].isnull().sum())

    print("\nCUSTOMER REVIEW ANALYSIS COMPLETED!")
    
    
    # ==================================
    # 14. EXPORT DATASETS FOR POWER BI
    # ==================================

    import os

    print("\n========== EXPORTING DATASETS ==========")

    # Create processed data folder
    output_folder = os.path.join(
        "data",
        "processed"
    )

    os.makedirs(output_folder, exist_ok=True)

    # Load sellers dataset
    sellers_df = pd.read_sql(
        "SELECT * FROM sellers",
        engine
    )

    # Datasets to export
    datasets = {
        "customers.csv": customers_df,
        "orders.csv": orders_df,
        "order_items.csv": order_items_df,
        "products.csv": products_df,
        "payments.csv": payments_df,
        "reviews.csv": reviews_df,
        "sellers.csv": sellers_df,
        "category_translation.csv": category_df,
        "sales_details.csv": sales_df
    }

    # Export each dataset
    for filename, dataframe in datasets.items():

        file_path = os.path.join(
            output_folder,
            filename
        )

        dataframe.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f"{filename} exported successfully | "
            f"Rows: {len(dataframe)}"
        )

    print("\nALL DATASETS EXPORTED SUCCESSFULLY!")


except Exception as e:
    print("Error:", e)

finally:
    engine.dispose()
