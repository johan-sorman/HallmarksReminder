from datetime import datetime
from version_update_scraper import get_version_update_date, insert_into_database, is_entry_exist_for_current_month
import schedule
import time

def main():
    base_url = "http://www.playonline.com/ff11us/campaign/login/login"
    url_number = 127

    now = datetime.now()
    url_number += (now.month + 126)
    url = f"{base_url}{url_number}.html"
    version_update_date = get_version_update_date(url)

    if version_update_date:
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if an entry with the same date already exists
        if is_entry_exist_for_current_month(version_update_date):
            print(f"Entry already exists for {version_update_date}. No new entry added.")
        else:
            insert_into_database(version_update_date, current_datetime)
            print(f"New entry added for {version_update_date}.")
    else:
        print("Unable to retrieve version update date.")
        print(url)

schedule.every().month.day.at("07:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)