import boto3
from typing import List, Tuple, Dict, Any

from tqdm import tqdm
from bs4 import BeautifulSoup
from lxml import etree

from src.env import MATCH_ID_QUEUE_URL
from src.scrape.bucket import Bucket
from src.scrape.web_driver import driver

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
	for region, tournament in tqdm(region_tournaments):
		driver.get('https://www.whoscored.com/Regions/%s/Tournaments/%s' % (region, tournament))
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		dom = etree.HTML(str(soup))
		for row in dom.xpath('//*[@id="tournament-fixture"]/div/div[@data-id]'):
			match_id = row.get('data-id')
			if bucket.contains('raw/%s.json.gzip' % match_id):
				continue
			queue.send_message(MessageBody=match_id)


if __name__ == '__main__':
	lambda_handler()
