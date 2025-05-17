import pandas as pd
from src import config

def load_data():
    try:
        crm_df = pd.read_csv(config.CRM_DATA_PATH)
        ecommerce_df = pd.read_csv(config.ECOMMERCE_DATA_PATH)
        website_df = pd.read_csv(config.WEBSITE_LOGS_PATH)
        print("Data loaded successfully.")
        return crm_df, ecommerce_df, website_df
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred during data loading: {e}")
        return None, None, None