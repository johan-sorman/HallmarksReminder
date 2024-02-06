from extract_update_info import extract_update_info
from database_operations import initialize_database, insert_update_info
import os
from dotenv import load_dotenv
import datetime
import time

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

while True:
    now = datetime.datetime.now()
    if now.day >= 1 and now.day <= 7:
        job()
    
    time.sleep(24 * 60 * 60)
