import pandas as pd

def save_dataframe(df, path):
    try:
        df.to_csv(path, index=False)
        print(f"DataFrame saved to {path}")
    except Exception as e:
        print(f"Error saving DataFrame to {path}: {e}")