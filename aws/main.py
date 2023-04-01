from aws_cdk import Stack, RemovalPolicy, App, CfnOutput
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class SharedInfrastructureStack(Stack):
	def __init__(self, scope: Construct):
		super().__init__(scope, 'soccer-analysis-shared-infrastructure')
		bucket = Bucket(self, 'bucket', removal_policy=RemovalPolicy.DESTROY)
		CfnOutput(self, 'bucket-output', export_name='bucket', value=bucket.bucket_name)
		CfnOutput(self, 'bucket-arn-output', export_name='bucket-arn', value=bucket.bucket_arn)


if __name__ == '__main__':
	app = App()
	SharedInfrastructureStack(app)
	app.synth()
