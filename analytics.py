import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_message_frequency_per_hour(db_path="bot_data.db"):
    """Returns message count grouped by hour."""
    conn = sqlite3.connect(db_path)
    query = """
        SELECT strftime('%Y-%m-%d %H:00:00', timestamp) AS hour, COUNT(*) AS message_count
        FROM messages
        GROUP BY hour
        ORDER BY hour;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_user_activity_summary(db_path="bot_data.db"):
    """Returns message count per user."""
    conn = sqlite3.connect(db_path)
    query = """
        SELECT user, COUNT(*) AS message_count
        FROM messages
        GROUP BY user
        ORDER BY message_count DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_channel_activity_summary(db_path="bot_data.db"):
    """Returns message count per channel."""
    conn = sqlite3.connect(db_path)
    query = """
        SELECT channel_id, COUNT(*) AS message_count
        FROM messages
        GROUP BY channel_id
        ORDER BY message_count DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_message_activity_heatmap(db_path="bot_data.db"):
    """Generates a heatmap of message activity per hour."""
    df = get_message_frequency_per_hour(db_path)

    # Convert hour column to datetime and extract hour
    df['hour'] = pd.to_datetime(df['hour'])
    df['hour_of_day'] = df['hour'].dt.hour

    # Pivot table for heatmap (assuming one day's data for simplicity)
    heatmap_data = df.pivot_table(values='message_count', index='hour_of_day', aggfunc='sum')

    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt="d", linewidths=0.5)
    plt.title("Message Activity Heatmap (Hourly)")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Message Count")
    plt.xticks(rotation=45)
    plt.show()

def plot_user_activity_bar_chart(db_path="bot_data.db"):
    """Generates a bar chart showing user activity."""
    df = get_user_activity_summary(db_path)

    plt.figure(figsize=(10, 6))
    plt.bar(df['user'], df['message_count'], color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Users")
    plt.ylabel("Message Count")
    plt.title("User Activity Summary")
    plt.show()

def plot_channel_activity_bar_chart(db_path="bot_data.db"):
    """Generates a bar chart showing channel activity."""
    df = get_channel_activity_summary(db_path)

    plt.figure(figsize=(10, 6))
    plt.bar(df['channel_id'], df['message_count'], color='lightcoral')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Channel ID")
    plt.ylabel("Message Count")
    plt.title("Channel Activity Summary")
    plt.show()
