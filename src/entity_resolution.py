import pandas as pd
import uuid

def create_master_customer_ids(crm_df, ecommerce_df, website_df):
    print("\nResolving Entities (Email-based)...")
    all_emails_list = []
    
    if crm_df is not None and not crm_df.empty and 'email_address' in crm_df.columns:
        all_emails_list.extend(crm_df['email_address'].dropna().unique().tolist())
    if ecommerce_df is not None and not ecommerce_df.empty and 'cust_email' in ecommerce_df.columns:
        all_emails_list.extend(ecommerce_df['cust_email'].dropna().unique().tolist())
    if website_df is not None and not website_df.empty and 'user_email' in website_df.columns:
        all_emails_list.extend(website_df['user_email'].dropna().unique().tolist())

    unique_emails = pd.Series(list(set(all_emails_list))).dropna().unique()
    
    if len(unique_emails) == 0:
        print("No valid emails found to create master customer profiles.")
        return pd.DataFrame(columns=['email', 'master_customer_id'])

    master_customer_df = pd.DataFrame({'email': unique_emails})
    master_customer_df['master_customer_id'] = [str(uuid.uuid4()) for _ in range(len(master_customer_df))]
    
    print(f"Created {len(master_customer_df)} unique master customer profiles.")
    return master_customer_df