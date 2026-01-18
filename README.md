# Big Query Client Explorer

A lightweight Streamlit application for exploring Google BigQuery datasets, running custom SQL queries, and visualizing query results with an interactive chart builder. The app emphasizes clarity, fast iteration, and a smooth workflow for both beginners and experienced developers.

## 🚀 Features

- Connects to **BigQuery** using service account credentials  
- Browse public datasets and view available tables  
- Run **custom SQL queries** directly in the app  
- Graceful SQL error handling (no crashes or state loss)  
- Visualize SQL query results using:
  - Scatter plots  
  - Line charts  
  - Bar charts  
- Chart Builder auto-detects numeric and categorical fields  
- Sidebar activates only after a successful SQL query  
- No BigQuery calls triggered by sidebar interactions  
- Plotting always uses the **SQL query output**, not dataset tables


## 🔧 Requirements

- Python 3.10+
- Streamlit
- Google Cloud BigQuery client
- A valid BigQuery service account key stored in `st.secrets["bigquery"]`

## ▶️ Running the App

Install dependencies:

```bash
pip install -r requirements.txt

streamlit run big_query_client_2.py
```

## .streamlit/secrets.toml

```
[bigquery]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
```