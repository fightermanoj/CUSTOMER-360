import pandas as pd

def profile_dataframe(df, df_name):
    if df is None or df.empty:
        print(f"\n--- Profiling for {df_name} ---")
        print(f"{df_name} is empty or None. Skipping profiling.")
        print("--- End Profiling ---")
        return

    print(f"\n--- Profiling for {df_name} ---")
    print("Shape:", df.shape)
    print("\nInfo:")
    df.info()
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDuplicates:", df.duplicated().sum())
    print("\nBasic Stats (for numeric columns):")
    numeric_cols = df.select_dtypes(include=['number']).columns
    if not numeric_cols.empty:
        print(df[numeric_cols].describe())
    else:
        print("No numeric columns to describe.")
    print("--- End Profiling ---")

def run_profiling(crm_df, ecommerce_df, website_df):
    profile_dataframe(crm_df, "CRM Data")
    profile_dataframe(ecommerce_df, "E-commerce Data")
    profile_dataframe(website_df, "Website Logs Data")