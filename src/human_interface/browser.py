from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

class BrowserHandler:
    def __init__(self, driver_path="chromedriver", browser_url="http://localhost"):
        self.driver = None
        self.driver_path = driver_path
        self.browser_url = browser_url

    def launch_browser(self):
        """Launches a browser window if not already launched."""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)  # Keeps browser open after script ends
            self.driver = webdriver.Chrome(service=ChromeService(self.driver_path), options=chrome_options)
            self.driver.get(self.browser_url)
            return "Browser has been launched successfully."
        else:
            return "Browser is already launched."

    def extract_html(self):
        """Extracts and returns the HTML content of the current page."""
        if self.driver:
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=" ", strip=True)
        else:
            return "Browser is not launched. Call launch_browser() first."


    def interact_with_page(self, css_selector, input_text=None):
        """
        Interacts with an element on the page.
        If input_text is provided, it will input text into the field specified by the CSS selector.
        """
        if not self.driver:
            return "Browser is not launched. Call launch_browser() first."
        
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            if input_text:
                element.clear()
                element.send_keys(input_text)
            else:
                element.click()
        except Exception as e:
            return f"Error interacting with page: {e}"

    def quit_browser(self):
        """Closes the browser if it's open."""
        if self.driver:
            self.driver.quit()
            self.driver = None