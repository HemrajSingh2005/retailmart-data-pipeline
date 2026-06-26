"""
=============================================================
RetailMart Pvt. Ltd. - Data Engineer Assignment
Submitted by: Hemraj Singh
=============================================================
"""



import pandas as pd
import numpy as np
import sqlite3
import os

# create sample csv files
def create_database():

    # products.csv
    products=pd.DataFrame({
        "product_id":['P001','P002','P003','P004','P005','P006','P007','P008','P009','P010'],

        'product_name': ['Basmati Rice 5kg','Sunflower Oil 1L','Toor Dal 1kg','Amul Butter 500g', 'Parle-G Biscuits', 'Maggi Noodles 4pk','Colgate Toothpaste', 'Surf Excel 1kg', 'Vim Dishwash Bar', 'Dettol Soap 3pk'],

        'category':['Staples', 'Edible Oil', 'Staples', 'Dairy', 'Snacks', 'Instant Food', 'Personal Care', 'Home Care', 'Home Care', 'Personal Care'],

        'price':[320.00, 145.00, 110.00, 230.00, 30.00, 55.00, 95.00, 220.00, 35.00, 85.00]
    })

    # stores.csv
    stores = pd.DataFrame({
        'store_id':   ['S01', 'S02', 'S03', 'S04', 'S05'],
        'store_name': ['RetailMart Jaipur Pink City', 'RetailMart Mumbai Andheri', 'RetailMart Delhi Karol Bagh', 'RetailMart Bengaluru Koramangala', 'RetailMart Chennai T Nagar'],

        'city':['Jaipur', 'Mumbai', 'Delhi', 'Bengaluru', 'Chennai'],

        'region':['North', 'West', 'North', 'South', 'South']
    })

    # sales_data.csv
    sales_data = pd.DataFrame({
        'sale_id':    ['TXN001', 'TXN002', 'TXN003', 'TXN004', 'TXN005',
                       'TXN006', 'TXN007', 'TXN008', 'TXN009', 'TXN010',
                       'TXN011', 'TXN012', 'TXN013', 'TXN002', 'TXN005'],  # last 2 are duplicates

        'store_id':   ['S01', 'S02', 'S03', 'S04', 'S05',
                       'S01', 'S02', 'S03', 'S04', 'S05',
                       'S01', 'S02', 'S03', 'S02', 'S05'],

        'product_id': ['P001', 'P002', 'P003', 'P004', 'P005',
                       'P006', 'P007', 'P008', 'P009', 'P010',
                       'P003', 'P001', 'P005', 'P002', 'P005'],

        'quantity':   [5, 3, None, 2, 10,
                       4, 1, 6, None, 8,
                       3, 7, 5, 3, 10],      # 2 missing values

        'sale_date':  ['2025-06-01', '2025-06-01', '2025-06-02', '2025-06-02', '2025-06-03', '2025-06-03', '2025-06-04', '2025-06-04', '2025-06-05', '2025-06-05','2025-06-06', '2025-06-06', '2025-06-07', '2025-06-01', '2025-06-03'],

        'amount':     [1600.0, 435.0, 330.0, 460.0, None,
                       220.0, 95.0, 1320.0, 70.0, 680.0,
                       330.0, 2240.0, 150.0, 435.0, None]  # 2 missing values
    })

    products.to_csv('products.csv', index=False)
    stores.to_csv('stores.csv', index=False)
    sales_data.to_csv('sales_data.csv', index=False)
    print(" ✅ Sample CSV files created: sales_data.csv, products.csv, stores.csv\n")

print("="*60)
print("MAIN PIPELINE")
print("="*60)

# main pipeline
def run_pipeline(): 

   # TASK 1: DATA INGESTION
    print("=" * 60)
    print("TASK 1: DATA INGESTION")
    print("=" * 60)

    try:
        sales_df = pd.read_csv("sales_data.csv")
        products_df = pd.read_csv("products.csv")
        stores_df = pd.read_csv("stores.csv")
    except FileNotFoundError as e:
        print(f"❌ Error: File not found — {e}")
        print("Please ensure that all CSV files exist in the working directory.")
    except pd.errors.EmptyDataError as e:
        print(f"❌ Error: One of the CSV files is empty — {e}")
    except sqlite3.Error as e:
        print(f"❌ Error: Database error — {e}")
    except Exception as e:
        print(f"❌ Error: Unexpected error in pipeline — {e}")

    # 1.1 shape and preview
    for name,df in [("sales_data", sales_df),
                    ("products", products_df),
                    ("stores", stores_df)]:
        print(f"\n📄 {name}.csv - Shape: {df.shape}")
        print(df.head())

    # 1.2 missing value summary
    print("\n🔍 Missing Value Summary:")
    for name,df in [("sales_data",sales_df),
                    ("products",products_df),
                    ("stores",stores_df)]:
        nulls=df.isnull().sum()
        nulls=nulls[nulls>0]
        if nulls.empty:
            print(f" {name}: No missing values")
        else:
            print(f" {name}:\n{nulls.to_string()}")


    # TASK 2: DATA CLEANING
    print("\n"+"="*60)
    print("Task 2: DATA CLEANING")
    print("="*60)

    # 2.3 Removing duplicate value
    before=len(sales_df)
    sales_df=sales_df.drop_duplicates()
    after=len(sales_df)
    print(f"\n🧹 Duplicates removed: {before-after} rows (Before: {before}, After: {after})")

    # 2.4 Filling missing quantity with 0, drop rows where amount is null
    sales_df["quantity"]=sales_df["quantity"].fillna(0)
    sales_df=sales_df.dropna(subset=['amount'])
    print(f"✅ After cleaning - Dataframe shape: {sales_df.shape}")
    print(sales_df)

    # 2.5 convert data types
    sales_df["sale_date"]=pd.to_datetime(sales_df["sale_date"])

    sales_df['amount']=sales_df['amount'].astype(float)
    print(f"\n✅ Data types after conversion:")
    print(sales_df.dtypes)


    # TASK 3: DATA TRANSFORMATION
    print("\n" + "=" * 60)
    print("TASK 3: DATA TRANSFORMATION")
    print("=" * 60)

    # 3.6 merge all three dataframes
    merged_df=sales_df.merge(stores_df, on='store_id',how='left')\
        .merge(products_df,on="product_id",how='left')
    print(f"\n✅ Merged DataFrame - Shape:{merged_df.shape}")
    print(merged_df.to_string())

    # 3.7 add total_revenue column using numpy
    merged_df['total_revenue']=merged_df['quantity']*merged_df['price']
    revenue=merged_df['total_revenue']
    print(f"\n💰 total_revenue stats:")
    print(f"Mean: ₹{np.mean(revenue):.2f}")
    print(f"Max: ₹{np.max(revenue):.2f}")
    print(f"Min: ₹{np.min(revenue):.2f}")

    # 3.8 revenue by city, sorted descending
    city_revenue=merged_df.groupby('city')['total_revenue']\
        .sum()\
        .sort_values(ascending=False)\
        .reset_index()
    city_revenue.columns=['city','total_revenue']
    print(f"\n🏙️ Total Revenue by City(Descending):")
    print(city_revenue.to_string(index=False))

    # TASK 4: DATA LOADING (SQL)
    print("\n" + "=" * 60)
    print("TASK 4: DATA LOADING TO SQLite")
    print("=" * 60)

    # 4.9 load into sqlite
    db_path='retailmart.db'
    conn=sqlite3.connect(db_path)
    merged_df.to_sql('retail_sales',conn,if_exists='replace', index=False)
    print(f"\n✅ Data loaded into SQLite database: '{db_path}' -> table: 'retail_sales' ")
    print(f" Rows inserted: {len(merged_df)}")

    # 4.10 top 3 best-selling products by total quantity
    query_top3="""SELECT product_name,SUM(quantity) AS total_quantity_sold
        FROM retail_sales
        GROUP BY product_name
        ORDER BY total_quantity_sold DESC 
        LIMIT 3
    """
    top3=pd.read_sql_query(query_top3,conn)
    print(f"\n🏆 Top 3 Best-Selling Products by Total Quantity:")
    print(top3.to_string(index=False))

    # TASK 5: REPORTING & INSIGHTS
    print("\n" + "=" * 60)
    print("TASK 5: REPORTING & INSIGHTS")
    print("=" * 60)
    
    # 5.11 revenue per store per day
    query_store_day="""
        SELECT store_name, sale_date, ROUND(SUM(total_revenue),2) AS daily_revenue
        FROM retail_sales
        GROUP BY store_name,sale_date
        ORDER BY store_name,sale_date
"""
    store_day_revenue=pd.read_sql_query(query_store_day,conn)
    print(f"\n📊 Total Revenue per Store per Day:")
    print(store_day_revenue.to_string(index=False))

    # 5.12 summary report
    total_transactions=len(merged_df)
    total_revenue=merged_df['total_revenue'].sum()
    top_city=city_revenue.iloc[0]['city']
    top_product=top3.iloc[0]['product_name']

    print(f"\n{'─'*40}")
    print(f"📋 RETAILMART SUMMARY REPORT")
    print(f"{'─'*40}")
    print(f"Total Transactions:{total_transactions}")
    print(f"Total Revenue:₹{total_revenue:,.2f}")
    print(f"Top Selling City:{top_city}")
    print(f"Top Selling Product:{top_product}")
    print(f"{'─'*40}")
    
    conn.close()
    print("\n✅ Pipeline completed successfully.")
    
if __name__ == "__main__":
    create_database()
    run_pipeline()
