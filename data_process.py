import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import re


def connect_database():
    """
    Connects to the database.
    """
    global conn
    conn = sqlite3.connect("hiking_data.db")
    print("Opened database successfully.")


def clean_table():
    """
    Cleans the provided table using Pandas.
    """
    df = pd.read_sql_query("SELECT * FROM hiking", conn)
    df = df.apply(lambda x: x.str.rstrip('m') if x.dtype == "object" else x)
    df = df.apply(lambda x: x.str.replace(',', '') if x.dtype == "object" else x)

    # For if I run this module again to test, I get AttributeError,
    # because ".astype('float')" will have already been applied.
    try:
        df['distance'] = df['distance'].str.rstrip('k')
    except AttributeError:
        pass
    df['distance'] = df['distance'].astype('float')

    cols_as_int = ['elevation_gain', 'elevation_loss', 'max_elevation', 'min_elevation']
    df[cols_as_int] = df[cols_as_int].astype('int')
    df.to_sql('hiking', conn, if_exists='replace', index=False)
    print('Table cleaned successfully.')


def convert_to_minutes(duration_str):
    """
    Converts data from "duration_str" column to minutes.
    """
    hours = minutes = 0
    hours_match = re.search(r'(\d+)\s*hours?', duration_str)
    minutes_match = re.search(r'(\d+)\s*minutes?', duration_str)
    if hours_match:
        hours = int(hours_match.group(1))
    if minutes_match:
        minutes = int(minutes_match.group(1))
    return hours * 60 + minutes


def sum_data():
    """
    Creates aggregated data.
    """
    df = pd.read_sql_query("SELECT * FROM hiking", conn)

    # Total distance:
    total_distance = df['distance'].sum()
    total_distance_rounded = round(total_distance, 2)
    print(f'Total distance: {total_distance_rounded} km.')

    # Total time:
    df['total_minutes'] = df['total_time'].apply(convert_to_minutes)
    total_time_minutes = df['total_minutes'].sum()
    total_hours = total_time_minutes // 60
    total_remaining_minutes = total_time_minutes % 60
    print(f'Total time: {total_hours} hours and {total_remaining_minutes} minutes.')


def plots():
    """
    Creates plots from hiking data.
    """
    df = pd.read_sql_query("SELECT * FROM hiking", conn)
    df.plot(kind='bar', x='id', y='distance', figsize=(10, 6), title='Distances per trail (km)')
    plt.savefig('dst_bar_plot.png')
    plt.show()


def main():
    print("Module 3:'data_process.py' is running")
    connect_database()
    clean_table()
    sum_data()
    plots()
    conn.close()
    print("Database connection closed.")


if __name__ == '__main__':
    main()
