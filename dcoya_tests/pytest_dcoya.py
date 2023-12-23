import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import ssl
import socket
import certifi

def check_ssl_certificate(hostname, port):
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = ssl_context.wrap_socket(socket.create_connection((hostname, port)), server_hostname=hostname)
        conn.settimeout(5.0)
        conn.do_handshake()

        ssl_info = conn.getpeercert()
        expiry_date_str = ssl_info.get('notAfter') or ssl_info.get('not_after') or ssl_info.get('expiry_date')
        if expiry_date_str:
            expiry_date = datetime.datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
        else:
            expiry_date = None

        current_date = datetime.datetime.now()
        days_until_expiry = (expiry_date - current_date).days if expiry_date else None

        protocol_version = conn.version()
        cipher_used = conn.cipher()
        print(protocol_version, cipher_used)
        return {
            'expiry_date': expiry_date,
            'current_date': current_date,
            'days_until_expiry': days_until_expiry,
            'ssl_info': ssl_info,
            'protocol_version': protocol_version,
            'cipher_used': cipher_used
        }

    except Exception as e:
        return {'error': f'SSL connection failed: {e}'}

@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


def test_website_response_code(browser):
    browser.get('https://dcoya:30000')
    assert browser.title == "Date and Machine Name"
    assert browser.current_url == "https://dcoya:30000/"  # Adjust URL to your actual site
    assert browser.page_source
    assert browser.find_element('tag name', 'body')


def test_machinename_and_datetime_exist(browser):
    browser.get('https://dcoya:30000')
    rendered_html = browser.page_source
    soup = BeautifulSoup(rendered_html, 'html.parser')

    date_element = soup.find('p', id='datetime')
    machine_element = soup.find('p', id='machinename')

    assert date_element is not None
    assert machine_element is not None


def test_date_format(browser):
    browser.get('https://dcoya:30000')
    rendered_html = browser.page_source
    soup = BeautifulSoup(rendered_html, 'html.parser')

    date_element = soup.find('p', id='datetime').get_text().split(':')[1].split(',')[0]
    assert date_element is not None

    current_date = datetime.datetime.now().strftime('%m/%d/%Y')
    assert date_element.strip() == f"{current_date}"

def test_ssl_certificate():
    hostname = 'dcoya'
    port = 30000

    ssl_details = check_ssl_certificate(hostname, port)
    expiry_date = ssl_details.get('expiry_date')
    current_date = ssl_details.get('current_date')
    days_until_expiry = ssl_details.get('days_until_expiry')
    protocol_version = ssl_details.get('protocol_version')
    cipher_used = ssl_details.get('cipher_used')[0]

    assert ssl_details.get('ssl_info') is not None, "SSL info is not retrieved."
    assert expiry_date > current_date, "Expiry date is not greater than the current date."
    assert days_until_expiry > 0, "Days until expiry is not greater than zero."
    assert protocol_version == "TLSv1.3"

    # List of secure cipher suites for TLSv1.3
    secure_ciphers = [
        'TLS_AES_128_GCM_SHA256',
        'TLS_AES_256_GCM_SHA384'
    ]

    assert cipher_used in secure_ciphers

