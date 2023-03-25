import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class Driver:
	def __init__(self):
		__options = Options()
		__options.add_argument("--headless")
		__options.add_argument(
			'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
		)
		self.__driver = webdriver.Chrome(options=__options)

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
