import pandas as pd
import sqlite3

def load_to_sql():
    conn = sqlite3.connect('ecom.db')

    # Load CSVs
    df1 = pd.read_csv('eligibility.csv')
    df2 = pd.read_csv('ad_sales.csv')
    df3 = pd.read_csv('total_sales.csv')

    print("eligibility.csv columns:", df1.columns)
    print("ad_sales.csv columns:", df2.columns)
    print("total_sales.csv columns:", df3.columns)

    # Save to SQL
    df1.to_sql('eligibility', conn, if_exists='replace', index=False)
    df2.to_sql('ad_sales', conn, if_exists='replace', index=False)
    df3.to_sql('total_sales', conn, if_exists='replace', index=False)

    conn.close()
    print("✅ All CSVs loaded into ecom.db")

if __name__ == "__main__":
    load_to_sql()
