import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src import config # Ensure this line is present and correct

st.set_page_config(
    page_title="Customer 360 Dashboard",
    layout="wide"
)

@st.cache_data
def load_data(file_path=config.OUTPUT_CSV_PATH): # Using config for the path
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)

            # Define columns and their expected types
            # String columns (fill NaN with empty string then convert to str)
            string_cols_expected = [
                'email', 'master_customer_id', 'first_name', 'last_name',
                'full_name_standardized', 'phone_standardized', 'crm_city',
                'signup_date', 'last_order_date'
                # 'segment' is handled separately below as it's categorical but read as str
            ]
            for col in string_cols_expected:
                if col in df.columns:
                    df[col] = df[col].fillna('').astype(str)
            
            # Segment column (categorical, ensure it's string for Plotly color mapping)
            if 'segment' in df.columns:
                df['segment'] = df['segment'].fillna('Unknown').astype(str)


            # Numeric columns (convert to numeric, coerce errors to NaN)
            numeric_cols_expected = [
                'total_spend', 'num_orders', 'total_time_spent_seconds',
                'days_since_last_order', 'num_sessions' # Assuming num_sessions is numeric
            ]
            for col in numeric_cols_expected:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Boolean column (handle various CSV representations)
            if 'is_vip' in df.columns:
                # Convert to string first to handle mixed types robustly, then map
                df['is_vip'] = df['is_vip'].astype(str).str.lower().map(
                    {'true': True, 'false': False, '1': True, '0': False, 
                     'yes': True, 'no': False, '1.0': True, '0.0': False, '': False, 'nan': False}
                ).fillna(False).astype(bool)

            return df
        except Exception as e:
            st.error(f"Error loading and processing data: {e}")
            return pd.DataFrame() # Return empty DataFrame on error
    else:
        st.warning(f"Data file '{file_path}' not found. Please run `main.py` first to generate it.")
        return pd.DataFrame()

df_360 = load_data()

st.title("Customer 360 Dashboard")
st.markdown("AI-Driven Data Integration Quality for Multi-Source Analytics Overview")

if not df_360.empty:
    st.header("Key Performance Indicators (KPIs)")
    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = df_360['master_customer_id'].nunique() if 'master_customer_id' in df_360.columns else 0
    total_spend = df_360['total_spend'].sum() if 'total_spend' in df_360.columns and df_360['total_spend'].notna().any() else 0.0
    avg_orders = df_360['num_orders'].mean() if 'num_orders' in df_360.columns and df_360['num_orders'].notna().any() else 0.0
    
    col1.metric("Total Unique Customers", f"{total_customers:,}")
    col2.metric("Total Revenue", f"${total_spend:,.2f}")
    col3.metric("Avg. Orders per Customer", f"{avg_orders:.2f}")

    if 'is_vip' in df_360.columns:
        # Ensure 'is_vip' is boolean before sum, as sum on boolean treats True as 1, False as 0
        vip_count = df_360['is_vip'].astype(bool).sum()
        col4.metric("VIP Customers", f"{vip_count:,}")
    else:
        col4.metric("VIP Customers", "N/A")

    st.markdown("---")

    if 'segment' in df_360.columns and df_360['segment'].nunique() > 0:
        st.header("Customer Segments Overview")
        
        segment_counts = df_360['segment'].value_counts().reset_index()
        # Ensure consistent column naming after value_counts and reset_index
        if 'index' in segment_counts.columns and 'segment' in segment_counts.columns and len(segment_counts.columns) == 2: # typical output
            segment_counts.columns = ['Segment', 'Number of Customers']
        elif len(segment_counts.columns) == 2: # Fallback if names are different but structure is same
            segment_counts.columns = ['Segment', 'Number of Customers']
        else: # If structure is unexpected, use a default
            st.warning("Segment counts structure unexpected. Using default column names.")
            segment_counts = pd.DataFrame({'Segment': [], 'Number of Customers': []})


        if not segment_counts.empty:
            fig_segment_dist = px.bar(segment_counts, 
                                      x='Segment', 
                                      y='Number of Customers', 
                                      title="Customer Distribution by Segment",
                                      color='Segment', # Plotly uses this for discrete colors
                                      text_auto=True)
            fig_segment_dist.update_layout(xaxis_title="Segment ID", yaxis_title="Number of Customers")
            st.plotly_chart(fig_segment_dist, use_container_width=True)

        if 'total_spend' in df_360.columns and df_360['total_spend'].notna().any():
            segment_spend = df_360.groupby('segment')['total_spend'].mean().reset_index()
            segment_spend.columns = ['Segment', 'Average Spend'] # Ensure consistent naming
            if not segment_spend.empty:
                fig_segment_spend = px.bar(segment_spend,
                                           x='Segment',
                                           y='Average Spend',
                                           title="Average Spend by Segment",
                                           color='Segment',
                                           text_auto=True)
                fig_segment_spend.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.2f')
                st.plotly_chart(fig_segment_spend, use_container_width=True)
    else:
        st.info("Segmentation data not available or not diverse enough for display.")

    st.markdown("---")
    st.header("Customer Data Explorer")
    
    display_df_main = df_360 # Default display
    if 'segment' in df_360.columns and df_360['segment'].nunique() > 0:
        unique_segments = ['All'] + sorted(df_360['segment'].unique().tolist())
        selected_segment = st.selectbox("Filter by Segment:", unique_segments)
        if selected_segment != 'All':
            display_df_main = df_360[df_360['segment'] == selected_segment]
    
    st.dataframe(display_df_main, use_container_width=True, height=400)

    st.subheader("Individual Customer Profile")
    if 'email' in df_360.columns and df_360['email'].notna().any():
        # Ensure email options are unique strings, handle potential NaNs from fillna('')
        email_options = [""] + sorted(df_360['email'][df_360['email'] != ''].astype(str).dropna().unique().tolist())
        selected_email = st.selectbox("Select Customer Email:", email_options)
        if selected_email: # Ensure selected_email is not an empty string
            customer_profile = df_360[df_360['email'] == selected_email]
            if not customer_profile.empty:
                st.write(customer_profile.T) # Transpose for better vertical display
            else:
                st.write("Customer not found.")
    else:
        st.write("Email column not available for customer lookup.")

    if st.checkbox("Show Raw Integrated Data (Sample)"):
        st.subheader("Raw Customer 360 Data (First 100 Rows)")
        st.dataframe(df_360.head(100), use_container_width=True)
else:
    st.error("No data to display. Ensure data pipeline has run and `customer_360_final.csv` exists.")

st.sidebar.info("Customer 360 Dashboard")
if st.sidebar.button("Re-run Data Pipeline (Instructions)"):
    st.sidebar.warning("Manual step: Please run `python main.py` in your terminal to refresh data.")