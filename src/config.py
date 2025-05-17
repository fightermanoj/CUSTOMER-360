import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

CRM_DATA_PATH = os.path.join(DATA_DIR, 'crm_data.csv')
ECOMMERCE_DATA_PATH = os.path.join(DATA_DIR, 'ecommerce_data.csv')
WEBSITE_LOGS_PATH = os.path.join(DATA_DIR, 'website_logs.csv')

FUZZY_MATCH_THRESHOLD = 85
MIN_ORDER_VALUE_FOR_VIP = 100
OUTPUT_CSV_PATH = os.path.join(BASE_DIR, "customer_360_final.csv")