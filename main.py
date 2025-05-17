from src import data_ingestion, data_profiling, data_cleansing
from src import entity_resolution, schema_mapping, data_enrichment
from src import customer_segmentation, utils, config
import pandas as pd

def main():
    print("Starting Customer 360 AI-Driven Data Integration Quality Project...")

    crm_df, ecommerce_df, website_df = data_ingestion.load_data()

    data_profiling.run_profiling(crm_df, ecommerce_df, website_df)

    crm_df_cleaned = data_cleansing.clean_crm_data(crm_df)
    ecommerce_df_cleaned = data_cleansing.clean_ecommerce_data(ecommerce_df)
    website_df_cleaned = data_cleansing.clean_website_data(website_df)

    master_customers = entity_resolution.create_master_customer_ids(
        crm_df_cleaned, ecommerce_df_cleaned, website_df_cleaned
    )

    customer_360_raw = schema_mapping.integrate_data(
        master_customers, crm_df_cleaned, ecommerce_df_cleaned, website_df_cleaned
    )

    customer_360_enriched = data_enrichment.enrich_customer_data(customer_360_raw)

    customer_360_final = customer_segmentation.segment_customers(customer_360_enriched)

    if customer_360_final is not None and not customer_360_final.empty:
        print("\n--- Final Customer 360 View (Sample) ---")
        print(customer_360_final.head())
        utils.save_dataframe(customer_360_final, config.OUTPUT_CSV_PATH)
    else:
        print("Final Customer 360 DataFrame is empty or None. Nothing to save or display.")

    print("\nProject execution finished.")

if __name__ == "__main__":
    main()