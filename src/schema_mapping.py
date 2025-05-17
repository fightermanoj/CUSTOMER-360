import pandas as pd

def integrate_data(master_customer_df, crm_df, ecommerce_df, website_df):
    print("\nIntegrating data...")
    if master_customer_df is None or master_customer_df.empty:
        print("Master customer DataFrame is empty. Cannot integrate.")
        return pd.DataFrame()

    customer_360_df = master_customer_df.copy()

    if crm_df is not None and not crm_df.empty and 'email_address' in crm_df.columns:
        crm_df_renamed = crm_df.rename(columns={'email_address': 'email', 'city': 'crm_city'})
        crm_cols_to_merge = ['email', 'first_name', 'last_name', 'full_name_standardized', 'phone_standardized', 'crm_city', 'signup_date']
        crm_cols_to_merge = [col for col in crm_cols_to_merge if col in crm_df_renamed.columns]
        if 'email' in crm_cols_to_merge:
             customer_360_df = pd.merge(customer_360_df, crm_df_renamed[crm_cols_to_merge], on='email', how='left')

    required_ecom_cols = ['email', 'order_value', 'order_date', 'order_id']
    if ecommerce_df is not None and not ecommerce_df.empty and 'cust_email' in ecommerce_df.columns:
        ecommerce_df_renamed = ecommerce_df.rename(columns={'cust_email': 'email'})
        if all(col in ecommerce_df_renamed.columns for col in required_ecom_cols):
            ecommerce_agg = ecommerce_df_renamed.groupby('email').agg(
                total_spend=('order_value', 'sum'),
                last_order_date=('order_date', 'max'),
                num_orders=('order_id', 'count')
            ).reset_index()
            customer_360_df = pd.merge(customer_360_df, ecommerce_agg, on='email', how='left')
        else:
            missing_cols = [col for col in required_ecom_cols if col not in ecommerce_df_renamed.columns]
            print(f"Skipping e-commerce aggregation due to missing columns: {missing_cols}")
            customer_360_df['total_spend'] = 0
            customer_360_df['last_order_date'] = pd.NaT
            customer_360_df['num_orders'] = 0
    else:
        customer_360_df['total_spend'] = 0
        customer_360_df['last_order_date'] = pd.NaT
        customer_360_df['num_orders'] = 0

    required_web_cols = ['email', 'time_spent_seconds', 'session_id']
    if website_df is not None and not website_df.empty and 'user_email' in website_df.columns:
        website_df_renamed = website_df.rename(columns={'user_email': 'email'})
        if all(col in website_df_renamed.columns for col in required_web_cols):
            website_agg = website_df_renamed.groupby('email').agg(
                total_time_spent_seconds=('time_spent_seconds', 'sum'),
                num_sessions=('session_id', 'nunique')
            ).reset_index()
            customer_360_df = pd.merge(customer_360_df, website_agg, on='email', how='left')
        else:
            missing_cols = [col for col in required_web_cols if col not in website_df_renamed.columns]
            print(f"Skipping website aggregation due to missing columns: {missing_cols}")
            customer_360_df['total_time_spent_seconds'] = 0
            customer_360_df['num_sessions'] = 0
    else:
        customer_360_df['total_time_spent_seconds'] = 0
        customer_360_df['num_sessions'] = 0
    
    cols_to_fill_zero = ['total_spend', 'num_orders', 'total_time_spent_seconds', 'num_sessions']
    for col in cols_to_fill_zero:
        if col in customer_360_df.columns:
            customer_360_df[col] = customer_360_df[col].fillna(0)
            
    print("Data integration complete.")
    return customer_360_df