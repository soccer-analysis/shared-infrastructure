from aws_cdk import Stack, RemovalPolicy, App, CfnOutput, Duration
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_sqs import Queue
from constructs import Construct

from aws.function import create_function, Allow


class MatchScraperStack(Stack):
	def __init__(self, scope: Construct):
		super().__init__(scope, 'soccer-analysis-match-scraper')
		match_id_queue = Queue(self, 'match-id-queue', retention_period=Duration.days(1),
							   visibility_timeout=Duration.minutes(15), receive_message_wait_time=Duration.seconds(20))
		bucket = Bucket(self, 'bucket', removal_policy=RemovalPolicy.DESTROY)

		create_function(
			self,
			name='backfill-match-ids',
			cmd='src.backfill_match_ids.lambda_handler',
			env={
				'BUCKET': bucket.bucket_name,
				'MATCH_ID_QUEUE_URL': match_id_queue.queue_url
			},
			memory_size=1024,
			reserved_concurrent_executions=1,
			allows=[
				Allow(
					actions=['s3:GetObject', 's3:ListBucket'],
					resources=[bucket.bucket_arn, f'{bucket.bucket_arn}/*']
				),
				Allow(
					actions=['sqs:SendMessage'],
					resources=[match_id_queue.queue_arn]
				)
			]
		)

		scrape_match = create_function(
			self,
			name='scrape-match',
			cmd='src.scrape_match.lambda_handler',
			env={
				'BUCKET': bucket.bucket_name
			},
			memory_size=512,
			reserved_concurrent_executions=100,
			allows=[
				Allow(
					actions=['s3:PutObject'],
					resources=[f'{bucket.bucket_arn}/*']
				)
			]
		)

		scrape_match.add_event_source(SqsEventSource(match_id_queue, batch_size=1))

		CfnOutput(self, 'match-id-queue-url', value=match_id_queue.queue_url)
		CfnOutput(self, 's3-bucket-output', value=bucket.bucket_name)


if __name__ == '__main__':
	app = App()
	MatchScraperStack(app)
	app.synth()
