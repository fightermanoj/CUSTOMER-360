import pandas as pd
import re
from nameparser import HumanName
import phonenumbers

def standardize_email(email_series):
    if email_series is None or not isinstance(email_series, pd.Series):
        return pd.Series(dtype='object')
    if not pd.api.types.is_string_dtype(email_series):
        email_series = email_series.astype(str)

    email_series = email_series.str.lower().str.strip()
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    valid_mask = email_series.str.match(email_regex, na=False)
    email_series_cleaned = email_series.copy()
    email_series_cleaned[~valid_mask] = None
    return email_series_cleaned

def standardize_names(name_series):
    if name_series is None or not isinstance(name_series, pd.Series):
        return pd.DataFrame(columns=['first_name', 'last_name', 'full_name_standardized'])
        
    parsed_names = []
    for name_str in name_series.fillna(""):
        if isinstance(name_str, str) and name_str.strip():
            try:
                name = HumanName(name_str)
                parsed_names.append({
                    'first_name': name.first.title() if name.first else None,
                    'last_name': name.last.title() if name.last else None,
                    'full_name_standardized': str(name).title() if str(name).strip() else None
                })
            except Exception:
                 parsed_names.append({'first_name': None, 'last_name': None, 'full_name_standardized': None})
        else:
            parsed_names.append({'first_name': None, 'last_name': None, 'full_name_standardized': None})
    return pd.DataFrame(parsed_names, index=name_series.index)

def standardize_phone(phone_series, region="US"):
    if phone_series is None or not isinstance(phone_series, pd.Series):
        return pd.Series(dtype='object')

    standardized_phones = []
    for p_num_str in phone_series.fillna(""):
        if isinstance(p_num_str, str) and p_num_str.strip():
            try:
                parsed_num = phonenumbers.parse(p_num_str, region)
                if phonenumbers.is_valid_number(parsed_num):
                    standardized_phones.append(phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.E164))
                else:
                    standardized_phones.append(None)
            except phonenumbers.NumberParseException:
                standardized_phones.append(None)
        else:
            standardized_phones.append(None)
    return pd.Series(standardized_phones, index=phone_series.index)

def clean_crm_data(crm_df):
    if crm_df is None or crm_df.empty:
        print("CRM data is empty or None. Skipping cleaning.")
        return pd.DataFrame()
    print("\nCleaning CRM Data...")
    df = crm_df.copy()
    if 'email_address' in df.columns:
        df['email_address'] = standardize_email(df['email_address'])
    if 'full_name' in df.columns:
        name_df = standardize_names(df['full_name'])
        df = pd.concat([df.drop(columns=['full_name'], errors='ignore'), name_df], axis=1)
    if 'phone' in df.columns:
        df['phone_standardized'] = standardize_phone(df['phone'])
        df.drop(columns=['phone'], inplace=True, errors='ignore')
    print("CRM Data cleaned.")
    return df

def clean_ecommerce_data(ecommerce_df):
    if ecommerce_df is None or ecommerce_df.empty:
        print("E-commerce data is empty or None. Skipping cleaning.")
        return pd.DataFrame()
    print("\nCleaning E-commerce Data...")
    df = ecommerce_df.copy()
    if 'cust_email' in df.columns:
        df['cust_email'] = standardize_email(df['cust_email'])
    print("E-commerce Data cleaned.")
    return df

def clean_website_data(website_df):
    if website_df is None or website_df.empty:
        print("Website data is empty or None. Skipping cleaning.")
        return pd.DataFrame()
    print("\nCleaning Website Data...")
    df = website_df.copy()
    if 'user_email' in df.columns:
        df['user_email'] = standardize_email(df['user_email'])
    print("Website Data cleaned.")
    return df