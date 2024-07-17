import time
import os
import sys
import sqlite3
import psutil


def close_database_connections(db_path):
    """
    Close any open connections to the SQLite database.
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
    except Exception as e:
        print(f"An error occurred while trying to close the database connection: {e}")


def force_close_database_connections(db_path):
    """
    Forcefully close any processes that have an open handle to the database file.
    """
    for proc in psutil.process_iter():
        try:
            for conns in proc.connections(kind='all'):
                if conns.laddr and conns.laddr.ip == '127.0.0.1' and conns.laddr.port == 8000:
                    proc.terminate()
                    proc.wait(timeout=5)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def delete_database_if_exists(db_path):
    """
    Deletes the database file if it exists, with retries if necessary.
    """
    if os.path.exists(db_path):
        close_database_connections(db_path)
        force_close_database_connections(db_path)
        for attempt in range(5):  # Retry up to 5 times
            try:
                os.remove(db_path)
                print(f"Deleted existing database at {db_path}")
                break
            except Exception as e:
                print(f"Attempt {attempt+1}: An error occurred while trying to delete the database: {e}")
                time.sleep(2)  # Wait before retrying
        else:
            print("Failed to delete the database after multiple attempts.")
            sys.exit(1)


if __name__ == '__main__':
    db_path = os.path.join(os.getcwd(), 'hiking_data.db')
    delete_database_if_exists(db_path)
