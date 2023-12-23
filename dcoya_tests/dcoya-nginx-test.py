from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import datetime


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')  # Add this line to ignore certificate errors


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get('https://dcoya:30000')  # Replace this with your URL

    rendered_html = driver.page_source
    soup = BeautifulSoup(rendered_html, 'html.parser')
    # Check for presence of date and machine name
    date_element = soup.find('p', id='datetime')
    machine_element = soup.find('p', id='machinename')
    if date_element and machine_element:
        print("Web page served correctly.")
        # Check the date
        current_date = datetime.datetime.now().strftime('%Y/%m/%d')
        print(current_date)
        if date_element.text.strip() == f"Current Local Date and Time: {current_date}":
            print(f"current_date: {current_date}")
            print("Date is correct.")
        else:
            print("Date is incorrect.")
    else:
        print("Web page elements not found.")

except Exception as e:
    print('Error:', e)

finally:
    driver.quit()

