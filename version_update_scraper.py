import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_version_update_date(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        entry = soup.find("p", class_="tx_topics")
        
        if entry:
            entry_text = entry.text.strip()
            match = re.search(r"The next version update is scheduled for (.+?)\.", entry_text)
            if match:
                scheduled_date = match.group(1)
                return scheduled_date
    except Exception as e:
        print("Error:", e)
    
    return None