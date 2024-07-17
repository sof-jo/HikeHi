import web_scraper
import conn_sqlite
import data_process
import time
import subprocess
import webbrowser
import os
import sys


def start_django_server():
    """
    Starts the Django local server.
    """
    try:
        manage_py = os.path.join(os.getcwd(), 'manage.py')
        print("Starting Django server...")
        server_process = subprocess.Popen([sys.executable, manage_py, "runserver"], shell=True)
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")
    return server_process


def main():
    """
    Runs the 3 modules to gather data and kml files, create and process the database, starts
    local server, opens web browser in /map page and closes the server.
    """
    try:
        # Run modules:
        print("Running module 1:'web_scraper'...")
        web_scraper.main()
        time.sleep(3)
        print("Running module 2:'conn_sqlite'...")
        conn_sqlite.main()
        time.sleep(3)
        print("Running module 3:'data_process'...")
        data_process.main()
        time.sleep(3)

        # Start server and visit page:
        server_process = start_django_server()  # Set for termination below
        webbrowser.open("http://127.0.0.1:8000/map")

        # Terminate server:
        input("Press Enter to stop the server...")
        server_process.terminate()
        server_process.wait()
        print("Django server stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
