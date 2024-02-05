from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import chromedriver_autoinstaller
import time
import sqlite3
from database_handler import insert_into_database, is_entry_exist_for_current_month

def get_version_update_date(url):
    chromedriver_autoinstaller.install()

    options = Options()
    options.headless = True
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        time.sleep(5)

        date_element = driver.find_element(By.XPATH, "//*[contains(text(), '[Campaign start]')]")

        if date_element:
            date_string = date_element.text.strip().replace('[Campaign start]', '').strip()
            date_string = date_string.rsplit(',', 1)[0].strip()
            extracted_date = datetime.strptime(date_string, "%A, %B %d, %Y").strftime("%Y-%m-%d")

            if not is_entry_exist_for_current_month(extracted_date):
                current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                insert_into_database(extracted_date, current_datetime)

            return extracted_date
    finally:
        driver.quit()

    return None