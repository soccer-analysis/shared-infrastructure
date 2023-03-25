install:
	rm -rf Pipfile.lock
	pipenv install -d

deploy:
	cdk deploy --require-approval never

scrape_season_match_ids:
	pipenv run python -m src.scrape.scrape_season_match_ids
