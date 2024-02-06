from extract_update_info import extract_update_info
from database_operations import initialize_database, insert_update_info
import os
from dotenv import load_dotenv
import schedule
import time
import datetime

load_dotenv()

def job():
    DB_PATH = os.getenv('DB_PATH')
    
    initialize_database(DB_PATH)
    
    url = "http://www.playonline.com/ff11us/index.shtml"
    scheduled_date = extract_update_info(url)
    
    if scheduled_date:
        insert_update_info(DB_PATH, scheduled_date)
    else:
        print("No entry found.")

schedule.every(24).hours.do(job)

def is_first_week_of_month():
    today = datetime.datetime.now()
    return today.day <= 7

if is_first_week_of_month():
    job()

while True:
    schedule.run_pending()
    time.sleep(1)