import pandas as pd
from src import config

def enrich_customer_data(customer_360_df):
    if customer_360_df is None or customer_360_df.empty:
        print("Customer 360 DataFrame is empty. Skipping enrichment.")
        return pd.DataFrame()
    print("\nEnriching customer data...")
    df = customer_360_df.copy()

    if 'total_spend' in df.columns:
        df['is_vip'] = df['total_spend'] > config.MIN_ORDER_VALUE_FOR_VIP
    else:
        df['is_vip'] = False

    if 'last_order_date' in df.columns:
        df['last_order_date'] = pd.to_datetime(df['last_order_date'], errors='coerce')
        if pd.api.types.is_datetime64_any_dtype(df['last_order_date']):
            df['days_since_last_order'] = (pd.Timestamp.now(tz=df['last_order_date'].dt.tz) - df['last_order_date']).dt.days
        else:
            df['days_since_last_order'] = pd.NA
    else:
        df['days_since_last_order'] = pd.NA
        
    print("Customer data enriched.")
    return df