import gzip
import random

import boto3
import botocore
import ujson
from typing import List, Tuple

import json5

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

from tqdm import tqdm
from unidecode import unidecode

from src.env import BUCKET

s3 = boto3.client('s3')

region_tournaments: List[Tuple[int, int]] = [
	(252, 2),  # Premier League
	(108, 5),  # Serie A
	(206, 4),  # LaLiga
	(81, 3),  # Bundesliga
	(74, 22),  # Ligue 1
	(250, 12),  # Champions League
	(250, 30)  # Europa League
]

options = Options()
options.add_argument("--headless")
options.add_argument(
	'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
)
driver = webdriver.Chrome(options=options)


def exists(key: str) -> bool:
	try:
		s3.head_object(Bucket=BUCKET, Key=key)
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			return False
		raise e
	return True


def wait(duration: float):
	time.sleep(duration)


def scrape_match(league_id: int, season: int, match_id: int) -> None:
	key = 'raw/%s.json.gzip' % match_id
	if exists(key):
		return
	driver.get('https://whoscored.com/Matches/%s/Live' % match_id)
	# wait(.25)
	raw = driver.page_source \
		.split('require.config.params["args"] = ')[-1] \
		.split('</script>')[0] \
		.replace(';', '') \
		.strip()
	data = json5.loads(unidecode(raw))
	if (data['matchCentreData'] or {}).get('elapsed') != 'FT':
		return
	data['league_id'] = league_id
	data['season'] = season
	compressed = gzip.compress(ujson.dumps(data).encode())
	s3.put_object(Bucket=BUCKET, Key=key, Body=compressed)


def main():
	league_season_match_ids: List[Tuple[int, int, int]] = []

	for region, tournament in tqdm(region_tournaments):
		driver.get('https://www.whoscored.com/Regions/%s/Tournaments/%s' % (region, tournament)),
		selected_season = driver.find_element(By.XPATH, '//select[@id="seasons"]//option[@selected="selected"]')
		current_season = int(selected_season.text.split('/')[0])
		while True:
			wait(.35)
			rows = driver.find_elements(
				By.XPATH,
				'//*[@id="tournament-fixture"]/div/div[@data-id]'
			)
			league_season_match_ids.extend([
				(tournament, current_season, int(x.get_attribute('data-id')))
				for x in rows
			])
			previous_day_button = driver.find_element(By.XPATH, '//a[contains(@class, "previous")]')
			is_disabled = 'is-disabled' in previous_day_button.get_attribute('class')
			if is_disabled:
				break
			previous_day_button.click()

	random.shuffle(league_season_match_ids)
	for league_id, _season, match_id in tqdm(league_season_match_ids):
		scrape_match(league_id, _season, match_id)


if __name__ == '__main__':
	main()
