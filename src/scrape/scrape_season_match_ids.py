import boto3
from typing import List, Tuple, Dict, Any
from tqdm import tqdm

from src.env import MATCH_ID_QUEUE_URL
from src.scrape.bucket import Bucket
from src.scrape.web_driver import Driver

region_tournaments: List[Tuple[int, int]] = [
	(252, 2),  # Premier League
	(108, 5),  # Serie A
	(206, 4),  # LaLiga
	(81, 3),  # Bundesliga
	(74, 22),  # Ligue 1
	(250, 12),  # Champions League
	(250, 30)  # Europa League
]


def lambda_handler(event: Dict = None, context: Any = None) -> None:
	bucket = Bucket()
	queue = boto3.resource('sqs').Queue(MATCH_ID_QUEUE_URL)
	driver = Driver()
	for region, tournament in tqdm(region_tournaments):
		driver.get('https://www.whoscored.com/Regions/%s/Tournaments/%s' % (region, tournament)).wait()
		while True:
			links = [
				x.get_attribute('href').lower()
				for x in driver.find_elements('//div[contains(@class, "result")]//a')
			]
			match_ids = list(set([x.split('/live/')[0].split('/matches/')[-1] for x in links if '/live/' in x]))
			for match_id in match_ids:
				if bucket.contains('raw/%s.json.gzip' % match_id):
					continue
				queue.send_message(MessageBody=match_id)
			previous_day_button = driver.find_element('//a[contains(@class, "previous")]')
			is_disabled = 'is-disabled' in previous_day_button.get_attribute('class')
			if is_disabled:
				break
			previous_day_button.click()
			driver.wait()


if __name__ == '__main__':
	lambda_handler()
