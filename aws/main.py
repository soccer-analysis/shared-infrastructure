from aws_cdk import Stack, RemovalPolicy, App, CfnOutput
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class SharedInfrastructureStack(Stack):
	def __init__(self, scope: Construct):
		super().__init__(scope, 'soccer-analysis-shared-infrastructure')
		data_lake_bucket = Bucket(self, 'data-lake-bucket', removal_policy=RemovalPolicy.DESTROY)
		CfnOutput(self, 'data-lake-bucket-output', export_name='data-lake-bucket', value=data_lake_bucket.bucket_name)
		CfnOutput(self, 'data-lake-bucket-arn-output', export_name='data-lake-bucket-arn',
				  value=data_lake_bucket.bucket_arn)


if __name__ == '__main__':
	app = App()
	SharedInfrastructureStack(app)
	app.synth()
