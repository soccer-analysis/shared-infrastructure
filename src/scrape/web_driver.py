import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class Driver:
	def __init__(self):
		options = Options()
		options.add_argument('--headless')
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--disable-gpu")
		options.add_argument("--disable-dev-tools")
		options.add_argument("--no-zygote")
		options.add_argument("--single-process")
		options.add_argument("window-size=2560x1440")
		options.add_argument("--user-data-dir=/tmp/chrome-user-data")
		options.add_argument("--remote-debugging-port=9222")
		options.add_argument(
			'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
		)
		self.__driver = webdriver.Chrome(
			options=options,
			service_log_path='/tmp/chromedriver.log'
		)

	def get(self, url: str) -> 'Driver':
		self.__driver.get(url)
		return self

	def find_element(self, xpath: str) -> WebElement:
		return self.__driver.find_element(By.XPATH, xpath)

	def find_elements(self, xpath: str) -> List[WebElement]:
		return self.__driver.find_elements(By.XPATH, xpath)

	def wait(self) -> 'Driver':
		time.sleep(.5)
		return self
