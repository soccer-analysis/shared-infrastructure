from typing import List, Tuple

from src.bucket import Bucket
from src.web_driver import Driver

region_tournaments: List[Tuple[int, int]] = [
	(74, 22),  # Ligue 1
	(81, 3),  # Bundesliga
	(108, 5),  # Serie A
	(206, 4),  # LaLiga
	(250, 12),  # Champions League
	(250, 30),  # Europa League
	(252, 2)  # Premier League
]


def enqueue_match_ids(driver: Driver, bucket: Bucket, queue) -> None:
	links = [
		x.get_attribute('href').lower()
		for x in driver.find_elements('//div[contains(@class, "result")]//a')
	]
	match_ids = list(set([x.split('/live/')[0].split('/matches/')[-1] for x in links if '/live/' in x]))
	for match_id in match_ids:
		if bucket.contains('raw/%s.json.gzip' % match_id):
			continue
		queue.send_message(MessageBody=match_id)
