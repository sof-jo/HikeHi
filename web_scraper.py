import glob
import os
import shutil
import time
import random
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import json

url_list = []
stats_data_list = []


def load_config(file_path: str):
    """
    Loads configuration JSON file, which user must input own Wikiloc username and password.
    Also, user must input src_folder path ("C:\\Users\\USER\\Downloads\\"),
    and dest_folder path ("C:\\Users\\USER\\PycharmProjects\\HikeHi\\map_app\\static\\kml_files\\").
    """
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


# Loads configuration from JSON file:
config = load_config(os.path.join(os.path.dirname(__file__), 'config.json'))
username = config['username']
password = config['password']
src_folder = config['src_folder']
dst_folder = config['dst_folder']


def driver_options():
    """
    Uses Chrome driver with options to keep the page running.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # Keeps running the page.
    global driver
    driver = webdriver.Chrome(options=options)


def login():
    """
    Logs in to Wikiloc account with provided credentials.
    Solve CAPTCHA manually (unfortunately).
    """
    driver_options()
    driver.get('https://www.wikiloc.com/wikiloc/start.do?')
    # Accept cookies:
    driver.find_element(By.XPATH, '/ html / body / div[1] / div / div / div / div[2] / div / button[1]').click()
    # Provide credentials:
    driver.find_element("id", "email").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    driver.find_element("id", "submit-button").click()
    time.sleep(10)  # Time to manually solve the CAPTCHA.


def get_url_list():
    """
    Searches all the pages while creating a list of partial urls of the trails to be used
    later as reference.
    """
    time.sleep(2)
    url_soup = BS(driver.page_source, 'html.parser')
    url_data = url_soup.find_all('a')
    for x in url_data:
        if x.get('href').startswith('/hiking-trails') and x.get('href') not in url_list:
            url_list.append(x.get('href'))
    print(f"{len(url_list)} urls found.")
    next_page()


def next_page():
    """
    Scrolls to the end of the page and then clicks next until it reaches the last page.
    """
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element(By.XPATH, '//img[@class="pagination__next-page"]').click()
        get_url_list()
    except NoSuchElementException:
        print(f"Finished searching the website for trails.\n{len(url_list)} kml files will start downloading now.")


def get_stats_and_files():
    """
    Opens each trail from the url list, gets the trail stats and downloads the kml files.
    Then converts the stats data into json object, moves downloaded kml files from default
    folder to destination. Finally, closes the browser.
    """
    for partial_url in url_list:
        driver.get('https://www.wikiloc.com' + partial_url)
        get_trail_stats(partial_url)
        get_kml_files()

    json_converter()
    time.sleep(2)
    mover()
    driver.close()
    print("Browser closed.")


def get_trail_stats(partial_url):
    """
    Gets the trail data using Beautifulsoup.
    """
    time.sleep(2)
    stats_soup = BS(driver.page_source, 'html.parser')

    def safe_find_next(soup, string, tag):
        element = soup.find(string=string)
        next_element = element.findNext(tag) if element else None
        return next_element.text if next_element else ""

    # Get trail data:
    trail_name = stats_soup.find('h1')
    distance = safe_find_next(stats_soup, 'Distance', 'dd')
    elevation_gain = safe_find_next(stats_soup, 'Elevation gain', 'dd')
    elevation_loss = safe_find_next(stats_soup, 'Elevation loss', 'dd')
    technical_difficulty = safe_find_next(stats_soup, 'Technical difficulty', 'dd')
    max_elevation = safe_find_next(stats_soup, 'Max elevation', 'dd')
    min_elevation = safe_find_next(stats_soup, 'Min elevation', 'dd')
    trail_type = safe_find_next(stats_soup, 'Trail type', 'dd')
    total_time = safe_find_next(stats_soup, 'Time', 'dd')
    recorded = safe_find_next(stats_soup, 'Recorded', 'dd')
    url = 'https://www.wikiloc.com' + partial_url

    # Create a list with dictionaries with the above trail data
    trail_data = {'trail_name': trail_name.text,
                  'distance': distance,
                  'elevation_gain': elevation_gain,
                  'elevation_loss': elevation_loss,
                  'technical_difficulty': technical_difficulty,
                  'max_elevation': max_elevation,
                  'min_elevation': min_elevation,
                  'trail_type': trail_type,
                  'total_time': total_time,
                  'recorded': recorded,
                  'url': url}
    stats_data_list.append(trail_data)


def get_kml_files():
    """
    Downloads kml files to default path ("C:/Users/sofas/Downloads").
    Couldn't solve how to change default path, so the kml files will be moved at a later step.
    """
    driver.find_element("id", "download-button").click()
    driver.find_element(By.XPATH, '//*[@href="#download-ge"]').click()
    driver.implicitly_wait(5)
    time.sleep(random.uniform(1, 3))
    driver.find_element(By.XPATH, '//*[@id="btn-download-ge"]').click()
    time.sleep(random.uniform(2, 5))  # Wait to start download and maybe avoid another CAPTCHA.


def json_converter():
    """
    Converts the stats_data_list (a list with dictionaries) into JSON file.
    """
    with open('hiking_data.json', 'w', encoding="utf-8") as file:
        json.dump(stats_data_list, file, indent=4, ensure_ascii=False)
    print(f"Json file 'hiking_data.json' has been created.")


def mover():
    """
    Moves downloaded kml files from default folder to destination.
    """
    counter = 0
    pattern = r"\*.kml"
    files = glob.glob(src_folder + pattern)
    for file in files:
        file_name = os.path.basename(file)
        shutil.move(file, dst_folder + file_name)
        counter += 1
    print(f'Moved {counter} kml files to {dst_folder}.')


def main():
    print("Module 1:'web_scraper.py' is running")
    login()
    get_url_list()
    get_stats_and_files()


if __name__ == "__main__":
    main()
