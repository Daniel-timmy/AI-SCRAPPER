import selenium.webdriver as webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

AUTH = os.getenv('AUTH')
SBR_WEBDRIVER = os.getenv('SBR_WEBDRIVER')

# def scrape_website(website):
#     print("Launching Chrome")
#     chrome_driver_path = "./chromedriver.exe"

#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

#     try:
#         driver.get(website)
#         print("Scraping website")
#         html = driver.page_source
#         time.sleep(5)
#         print("Scraping complete")
#         return html
#     finally:
#         driver.quit()


def scrape_website(website):
    print("Launching Chrome")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
        return html
    print('Scraping complete')

def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    if body is None:
        return "No body tag found"
    return str(body)

def clean_body_content(body):
    soup = BeautifulSoup(body, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = "\n".join(line.strip() 
                                 for line in cleaned_content.split() if line.strip())
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)]