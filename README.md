HikeHi is a Python-based project designed for hiking enthusiasts to help them visualize and analyze their hiking trails. The application collects data from the Wikiloc website, specifically from the hiking trails uploaded by a user with their credentials, and displays this data along with a map of the routes on a webpage. It is a full stack web development project, involving web scraping, data cleaning and processing, database creation, and the creation of an interactive website. 

This project was developed on July 2024 for HAEC Python seminar in Athens Greece with Python 3.12, and it's used for educational purposes.

Libraries used:
Selenium, BeautifulSoup, Pandas, Matplotlib, Django.

How to use:
1. Install the libraries mentioned above.
2. Please fill the config.json file with your Wikiloc credentials, default download folder path (for example: "C:\\Users\\USER\\Downloads\\") and destination folder path (for example: "C:\\Users\\USER\\PycharmProjects\\HikeHi\\map_app\\static\\kml_files\\").
3. Finally run the main_script.py module.

Additionaly, 
1. If you want to delete everything to start anew and can't delete the database please run kill_db.py module.
2. If you have already run the main_script.py module and only want to see the /map webpage, please open main_script.py module, disable the modules under "#Run modules:".
3. Downloading kml files takes a few minutes, so if you just want to test this project, in order to save time, open web_scraper.py, go to "def get_url_list():" and disable "next_page()". This should find and download a maximum of 10 hiking trails.

How it works:
1. Web scraping (web_scraper.py):
Log in to Wikiloc, solve the captcha manually unfortunately. Selenium (with Chromedriver) is used to automate the login process, searches all the hiking trails, and saves the URLs of each route to navigate through the entire website. Then it opens each route and uses BeautifulSoup to get the route data and Selenium again to download and move the kml file to a specific folder (which is used later by Django). The data from the soup format is converted to JSON.
Creates the file “hiking_data.json”.
2. Database creation (conn_sqlite.py):
Opens and cleans the JSON file from NBSP characters, creates the database “hiking_data” and transfers the route data to the table “hiking”, using the relational database SQLite.
Creates the file “hiking_data.db”.
3. Data processing (data_process.py):
Uses Pandas and Matplotlib. Initially cleans and processes the "hiking" table. So far, it calculates the total distance and total hiking time, and prints a bar chart with the distances of the routes.
Creates the file "dst_bar_plot.png".
4. Web application development:
Uses Django to to start a local basic web server. So far, the only view is in the “map_app” directory, where in map_app/templates I wrote the "map.html" which loads the logo, the kml files from map_app/static and the hiking data, and displays all of them on one map. Finally it opens http://127.0.0.1:8000/map page, where you can change the map background and by hovering over a trail you can see the data for that trail. 

Enjoy :)
