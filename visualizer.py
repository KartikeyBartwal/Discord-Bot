import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

db_path = "bot_data.db"

def get_connection():
    return sqlite3.connect(db_path)

def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def get_table_data(table_name):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def get_message_frequency_per_hour():
    conn = get_connection()
    query = """
        SELECT strftime('%H', timestamp) AS hour, COUNT(*) AS message_count
        FROM messages
        GROUP BY hour
        ORDER BY hour;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_user_activity_summary():
    conn = get_connection()
    query = """
        SELECT user, COUNT(*) AS message_count
        FROM messages
        GROUP BY user
        ORDER BY message_count DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_channel_activity_summary():
    conn = get_connection()
    query = """
        SELECT channel_id, COUNT(*) AS message_count
        FROM messages
        GROUP BY channel_id
        ORDER BY message_count DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_message_activity_heatmap():
    df = get_message_frequency_per_hour()
    df['hour'] = df['hour'].astype(int)
    plt.figure(figsize=(10, 5))
    sns.heatmap(df.pivot_table(index='hour', values='message_count', aggfunc='sum'), annot=True, fmt="d", cmap='coolwarm')
    plt.title("Message Activity Heatmap")
    st.pyplot(plt)

def plot_user_activity_bar_chart():
    df = get_user_activity_summary()
    plt.figure(figsize=(10, 5))
    sns.barplot(x='message_count', y='user', data=df.head(10), palette='viridis')
    plt.title("Top 10 Active Users")
    st.pyplot(plt)

def plot_channel_activity_bar_chart():
    df = get_channel_activity_summary()
    plt.figure(figsize=(10, 5))
    sns.barplot(x='message_count', y='channel_id', data=df.head(10), palette='plasma')
    plt.title("Top 10 Active Channels")
    st.pyplot(plt)

st.title("📊 Discord Bot Database & Analytics Viewer")

tables = get_tables()
if not tables:
    st.warning("No tables found in the database.")
else:
    selected_table = st.selectbox("Select a table:", tables)
    df = get_table_data(selected_table)
    st.write(f"### Data from `{selected_table}` table:")
    st.dataframe(df)

st.write("## 📈 Analytics & Visualizations")
if st.button("Show Message Activity Heatmap"):
    plot_message_activity_heatmap()
if st.button("Show User Activity Bar Chart"):
    plot_user_activity_bar_chart()
if st.button("Show Channel Activity Bar Chart"):
    plot_channel_activity_bar_chart()
