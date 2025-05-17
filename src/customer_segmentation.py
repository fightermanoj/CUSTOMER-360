import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

def segment_customers(customer_360_df, n_clusters=3):
    if customer_360_df is None or customer_360_df.empty:
        print("Customer 360 DataFrame is empty. Skipping segmentation.")
        return pd.DataFrame()
    print("\nSegmenting customers...")
    df = customer_360_df.copy()

    features = []
    if 'total_spend' in df.columns: features.append('total_spend')
    if 'num_orders' in df.columns: features.append('num_orders')
    if 'total_time_spent_seconds' in df.columns: features.append('total_time_spent_seconds')
    
    if not features:
        print("Not enough features for segmentation. Assigning default segment.")
        df['segment'] = 'default'
        return df

    segment_data = df[features].copy()
    for col in features:
        segment_data[col] = pd.to_numeric(segment_data[col], errors='coerce').fillna(0)

    if segment_data.empty or (segment_data == 0).all().all() or len(segment_data) < n_clusters:
        print("Insufficient or non-variable data for clustering. Assigning default segment.")
        df['segment'] = 'default'
        return df
        
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(segment_data)
    
    actual_n_clusters = min(n_clusters, len(np.unique(scaled_features, axis=0)))
    if actual_n_clusters < 1: # needs at least 1 cluster
        print(f"Not enough distinct data points for {n_clusters} clusters. Assigning to default segment.")
        df['segment'] = 'default'
        return df
    if actual_n_clusters == 1: # KMeans needs at least 2 for typical use, but handle 1
         df['segment'] = 0 
         print(f"Only one distinct group found. Assigning all to segment 0.")
         return df


    kmeans = KMeans(n_clusters=actual_n_clusters, random_state=42, n_init='auto')
    try:
        df['segment'] = kmeans.fit_predict(scaled_features)
    except Exception as e:
        print(f"Error during Kmeans fitting: {e}. Assigning default segment.")
        df['segment'] = 'error_default'
    
    print("Customer segmentation complete.")
    return df