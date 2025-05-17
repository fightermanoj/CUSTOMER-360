## Project By Manoj Gowda R CAN ID - CAN_35654482 
# AI-Driven Customer 360 & Personalized Marketing Analytics

This project demonstrates an end-to-end pipeline for creating a Customer 360 view from multi-source data. It leverages AI-driven techniques for data integration quality, followed by analytics for customer segmentation and personalized marketing insights. The project includes a data processing pipeline, a Streamlit-based visual dashboard, and a Jupyter Notebook for exploratory analysis.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
  - [1. Data Processing Pipeline](#1-data-processing-pipeline)
  - [2. Streamlit Visual Dashboard](#2-streamlit-visual-dashboard)
  - [3. Jupyter Notebook Dashboard](#3-jupyter-notebook-dashboard)
- [Data Sources (Simulated)](#data-sources-simulated)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The core objective is to consolidate customer data from disparate sources (CRM, e-commerce, website logs) into a unified, high-quality dataset. This "Customer 360" view enables advanced analytics, such as customer segmentation, which can then be used to drive personalized marketing strategies. The project emphasizes the importance of AI-driven data quality assurance throughout the integration process.

## Features

1.  **Data Ingestion:** Loads data from multiple CSV sources.
2.  **Data Profiling:** Generates basic statistics and identifies quality issues in raw data.
3.  **AI-Driven Data Cleansing:**
    *   Standardizes names, email formats, and phone numbers.
    *   Utilizes libraries with pattern recognition capabilities (e.g., `nameparser`, `phonenumbers`).
4.  **Entity Resolution:** Identifies unique customers across sources, primarily using standardized email addresses.
5.  **Schema Mapping & Integration:** Merges cleansed data into a unified Customer 360 schema.
6.  **Data Enrichment:** Derives new features (e.g., VIP status, days since last order).
7.  **Customer Segmentation:** Applies K-Means clustering (unsupervised ML) to segment customers based on behavioral data.
8.  **Visualization & Reporting:**
    *   Interactive Streamlit dashboard for KPIs, segment analysis, and customer exploration.
    *   Jupyter Notebook for detailed exploratory data analysis and reporting.

## Technology Stack

*   **Programming Language:** Python 3.9+
*   **Core Data Manipulation:** Pandas, NumPy
*   **Data Cleansing & Validation:** `nameparser`, `python-phonenumbers`, `fuzzywuzzy`
*   **Machine Learning (Segmentation):** Scikit-learn
*   **Visual Dashboard:** Streamlit, Plotly Express
*   **Notebook Dashboard:** Jupyter Notebook, Matplotlib, Seaborn, ipywidgets
*   **Environment Management:** Python Virtual Environments (e.g., `venv`)

## Project Structure

```
customer_360_project/
├── data/                     # Raw input data files
│   ├── crm_data.csv
│   ├── ecommerce_data.csv
│   └── website_logs.csv
├── src/                      # Source code for the data pipeline
│   ├── __init__.py
│   ├── config.py             # Configuration (file paths, thresholds)
│   ├── data_ingestion.py
│   ├── data_profiling.py
│   ├── data_cleansing.py
│   ├── entity_resolution.py
│   ├── schema_mapping.py
│   ├── data_enrichment.py
│   ├── customer_segmentation.py
│   └── utils.py              # Utility functions (e.g., saving data)
├── main.py                   # Main script to run the data processing pipeline
├── dashboard_streamlit.py    # Streamlit application for visual dashboard
├── dashboard_notebook.ipynb  # Jupyter Notebook for exploratory dashboard
├── customer_360_final.csv    # Output: Processed and integrated customer data
└── requirements.txt          # Python package dependencies
```

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd customer_360_project
    ```

2.  **Create and Activate a Virtual Environment:**
    (Recommended to avoid conflicts with system-wide packages)
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare Data:**
    Ensure your source CSV files (`crm_data.csv`, `ecommerce_data.csv`, `website_logs.csv`) are placed in the `data/` directory. Refer to the [Data Sources (Simulated)](#data-sources-simulated) section for expected formats. Example files are provided.

## Running the Project

Follow these steps in order:

### 1. Data Processing Pipeline

This step ingests raw data, performs cleaning and integration, and generates the `customer_360_final.csv` file, which is used by the dashboards.

Navigate to the project root directory (`customer_360_project/`) in your terminal and run:
```bash
python main.py
```
Upon successful execution, a `customer_360_final.csv` file will be created in the project root.

### 2. Streamlit Visual Dashboard

This launches an interactive web application for visualizing KPIs, customer segments, and exploring individual customer profiles.

Ensure the data processing pipeline (`main.py`) has been run successfully. Then, from the project root directory, execute:
```bash
streamlit run dashboard_streamlit.py
```
The dashboard will typically open automatically in your default web browser (e.g., at `http://localhost:8501`).

### 3. Jupyter Notebook Dashboard

This provides a notebook environment for more detailed exploratory analysis and static report generation.

Ensure the data processing pipeline (`main.py`) has been run successfully. Then, from the project root directory, start Jupyter:
```bash
# If you prefer Jupyter Notebook
jupyter notebook

# Or, if you prefer JupyterLab
jupyter lab
```
Once Jupyter opens in your browser, navigate to and open `dashboard_notebook.ipynb`. Run the cells sequentially to generate the analyses and visualizations.

## Data Sources (Simulated)

The project uses three simulated CSV data sources placed in the `data/` directory:

*   **`crm_data.csv`**:
    *   Columns: `customer_id`, `full_name`, `email_address`, `phone`, `city`, `signup_date`
*   **`ecommerce_data.csv`**:
    *   Columns: `order_id`, `cust_email`, `product_name`, `order_date`, `order_value`, `shipping_address`
*   **`website_logs.csv`**:
    *   Columns: `session_id`, `user_email`, `page_visited`, `visit_timestamp`, `time_spent_seconds`

Populate these files with sample data, including some inconsistencies or missing values, to observe the effects of the data quality and integration processes.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Open a Pull Request.

Please ensure your code adheres to good practices and includes relevant documentation or tests where applicable.

## License

This project is licensed under the MIT License. See the `LICENSE` file (if one were present, typically you'd add one) for details. For now, consider it open for use and modification.
```

**Important Considerations for a Real GitHub README:**

*   **LICENSE File:** You would typically include an actual `LICENSE` file (e.g., `LICENSE.md`) in your repository root, choosing an appropriate open-source license like MIT, Apache 2.0, etc.
*   **Screenshots/GIFs:** For a truly professional README, adding a screenshot of the Streamlit dashboard or a GIF demonstrating its interactivity would be highly beneficial.
*   **Detailed Feature Explanation:** You might expand on what each "AI-Driven" aspect truly entails for a more technical audience.
*   **Testing:** Mentioning how to run tests (if you had a test suite) would be standard.
*   **Deployment:** If the project were meant for deployment, a section on deployment options (e.g., Streamlit Cloud, Docker) would be included.
*   **Contact/Support:** Information on how to get support or contact maintainers.

This generated README provides a solid, professional foundation.
