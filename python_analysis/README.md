# Python Analysis – E-Commerce Sales

## Overview
This folder contains Python scripts used to explore and analyse the Olist Brazilian E-Commerce dataset.

## Technologies Used
- Python
- Pandas
- SQLAlchemy
- PyMySQL
- MySQL

## Analysis Performed
- Customer analysis
- Order and delivery analysis
- Product and category analysis
- Payment analysis
- Customer review analysis
- Sales data processing

## Database Connection
The Python script connects to the MySQL database `ecommerce_analytics` using credentials stored in a `.env` file.

## How to Run

1. Install Python.
2. Install the required libraries:

   `pip install -r requirements.txt`

3. Configure your MySQL credentials in the project's `.env` file.
4. Make sure the MySQL database and required tables are available.
5. Run the analysis:

   `python mysql_connection.py`

## Output
Processed analysis datasets are exported as CSV files into the `data/processed` folder.