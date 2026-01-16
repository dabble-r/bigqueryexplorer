from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
import db_dtypes as dbt
import pandas as pd


# Construct a BigQuery client object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["bigquery"]
)


@st.cache_resource
def get_bigquery_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["bigquery"]
    )
    return bigquery.Client(credentials=credentials, project=credentials.project_id)

client = get_bigquery_client()

st.title("Big Query Client")

#@st.cache_data
def run_query(query: str):
    client = get_bigquery_client()
    rows = client.query_and_wait(query)  # Make an API request.
    df = rows.to_dataframe()
    return df

def query_handler(query: str):
    if query == "":
        st.error("Please enter a query")
        return None
    df = run_query(query)
    st.success("Query executed successfully")
    st.dataframe(df)


query_2 = st.text_area(label="query", value="", height="content", max_chars=None, key=None, help=None, 
                       on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, 
                       label_visibility="visible", width="stretch")

submit_btn = st.button(label="submit", key=None, help=None, on_click=lambda: query_handler(query_2), args=None, kwargs=None, 
                       type="secondary", icon=None, disabled=False, use_container_width=None, 
                       width="content", shortcut=None)
