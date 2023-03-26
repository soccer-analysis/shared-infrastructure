install:
	rm -rf Pipfile.lock
	pipenv install -d

deploy:
	cdk deploy --require-approval never

scrape_season_match_ids:
	pipenv run python -m src.scrape.scrape_season_match_ids

local:
	docker buildx build -t soccer-analysis:latest --platform linux/amd64 .
	docker ps -aq | xargs docker stop
	docker run -d -p 9000:8080 --env-file .env soccer-analysis:latest src.scrape.scrape_season_match_ids.lambda_handler
	sleep 1
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

test:
	docker buildx build -t soccer-analysis-test:latest -f Dockerfile.test --platform linux/amd64 .
	docker ps -aq | xargs docker stop
	docker run soccer-analysis-test:latest