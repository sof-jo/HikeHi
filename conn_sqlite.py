import re
import sqlite3
import json


def open_json():
    global json_data
    with open('hiking_data.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)


def clean_json():
    """
    Cleans data of the provided json file.
    """
    open_json()
    # print("Original data:", json_data)

    def replace_nbsp(data):
        """
        Replaces NBSP in provided json file.
        """
        if isinstance(data, dict):
            return {key: replace_nbsp(value) for key, value in data.items()}
            pass
        elif isinstance(data, list):
            return [replace_nbsp(element) for element in data]
        elif isinstance(data, str):
            return data.replace('\u00A0', '').replace('&nbsp;', '')
        else:
            return data

    cleaned_data = replace_nbsp(json_data)
    # print("Cleaned data:", cleaned_data)
    with open('hiking_data.json', 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)
    print("File cleaned successfully.")


def connect_to_sqlite_database():
    """
    Creates the sqlite database for storing hike data.
    """
    conn = sqlite3.connect("hiking_data.db")
    print("Opened database successfully.")
    try:
        conn.execute('''CREATE TABLE hiking
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 kml_file_name TEXT NOT NULL,
                 trail_name TEXT NOT NULL,
                 distance TEXT NOT NULL,
                 elevation_gain TEXT NOT NULL,
                 elevation_loss TEXT NOT NULL,
                 technical_difficulty TEXT NOT NULL,
                 max_elevation TEXT NOT NULL,
                 min_elevation TEXT NOT NULL,
                 trail_type TEXT NOT NULL,
                 total_time TEXT NOT NULL,
                 recorded TEXT NOT NULL,
                 url TEXT NOT NULL);''')
        print("Table created successfully.")
    except sqlite3.OperationalError as a:
        print(f"WARNING: {a}")
    return conn


def populate_table(db_conn, data):
    """
    Populates hiking table with provided data.
    """
    for entry in data:
        trail_name = entry["trail_name"]
        distance = entry["distance"]
        elevation_gain = entry["elevation_gain"]
        elevation_loss = entry["elevation_loss"]
        technical_difficulty = entry["technical_difficulty"]
        max_elevation = entry["max_elevation"]
        min_elevation = entry["min_elevation"]
        trail_type = entry["trail_type"]
        total_time = entry["total_time"]
        recorded = entry["recorded"]
        url = entry["url"]
        kml_file_name = extract_kml_file_name(url)

        sql_str = '''INSERT INTO hiking (
                        kml_file_name, trail_name, distance, elevation_gain, elevation_loss,
                        technical_difficulty, max_elevation, min_elevation,
                        trail_type, total_time, recorded, url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        # print(sql_str)
        try:
            db_conn.execute(sql_str, (
                kml_file_name, trail_name, distance, elevation_gain, elevation_loss,
                technical_difficulty, max_elevation, min_elevation,
                trail_type, total_time, recorded, url
            ))
        except sqlite3.IntegrityError as i:
            print(i)
    db_conn.commit()


def extract_kml_file_name(url):
    pattern = r'/([^/]+)-\d+$'
    match = re.search(pattern, url)
    if match:
        kml_file_name = match.group(1)
    else:
        kml_file_name = ''
    return kml_file_name


def main():
    print("Module 2:'conn_sqlite.py' is running")
    clean_json()
    open_json()
    db_connection = connect_to_sqlite_database()
    populate_table(db_connection, json_data)
    db_connection.close()
    print("Database connection closed.")


if __name__ == "__main__":
    main()
