from os import getcwd
from typing import cast

from aws_cdk import Stack, RemovalPolicy, App, CfnOutput, Duration
from aws_cdk.aws_ecr_assets import Platform
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, Function
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_sqs import Queue
from constructs import Construct


class SoccerAnalysisStack(Stack):
	def __init__(self, scope: Construct):
		super().__init__(scope, 'soccer-analysis')
		match_id_queue = Queue(self, 'match-id-queue')
		bucket = Bucket(self, 'bucket', removal_policy=RemovalPolicy.DESTROY)

		scrape_match_ids: Function = DockerImageFunction(
			self,
			'scrape-season-match-ids-function',
			function_name='scrape-season-match-ids',
			reserved_concurrent_executions=1,
			memory_size=1024,
			timeout=Duration.minutes(15),
			log_retention=RetentionDays.FIVE_DAYS,
			code=DockerImageCode.from_image_asset(
				directory=getcwd(),
				platform=cast(Platform, Platform.LINUX_AMD64),
				file='Dockerfile',
				cmd=['src.scrape.scrape_season_match_ids.lambda_handler']
			),
			environment={
				'BUCKET': bucket.bucket_name,
				'MATCH_ID_QUEUE_URL': match_id_queue.queue_url
			},
			role=Role(
				self,
				'scrape-match-ids-role',
				role_name='place-trades',
				assumed_by=ServicePrincipal('lambda.amazonaws.com'),
				managed_policies=[
					ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
				],
				inline_policies={
					'Policies': PolicyDocument(statements=[
						PolicyStatement(
							effect=Effect.ALLOW,
							actions=[
								's3:GetObject',
								's3:ListBucket'
							],
							resources=[
								bucket.bucket_arn,
								f'{bucket.bucket_arn}/*'
							]
						),
						PolicyStatement(
							effect=Effect.ALLOW,
							actions=[
								'sqs:SendMessage',
							],
							resources=[
								match_id_queue.queue_arn
							]
						)
					])
				}
			)
		)

		CfnOutput(self, 'match-id-queue-url', value=match_id_queue.queue_url)
		CfnOutput(self, 's3-bucket-output', value=bucket.bucket_name)


if __name__ == '__main__':
	app = App()
	SoccerAnalysisStack(app)
	app.synth()
