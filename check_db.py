import streamlit as st
import sqlite3
import pandas as pd

# Database file path
db_path = "bot_data.db"

# Connect to database
def get_connection():
    return sqlite3.connect(db_path)

# Fetch table names
def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

# Fetch data from a selected table
def get_table_data(table_name):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Streamlit UI
st.title("📊 Discord Bot Database Viewer")

# Load tables
tables = get_tables()
if not tables:
    st.warning("No tables found in the database.")
else:
    selected_table = st.selectbox("Select a table:", tables)
    df = get_table_data(selected_table)
    st.write(f"### Data from `{selected_table}` table:")
    st.dataframe(df)
