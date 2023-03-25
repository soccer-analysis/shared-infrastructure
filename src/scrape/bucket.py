import boto3
import botocore

from src.env import BUCKET


class Bucket:
	def __init__(self):
		self.__s3 = boto3.client('s3')

	def contains(self, key: str) -> bool:
		try:
			self.__s3.head_object(Bucket=BUCKET, Key=key)
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == '404':
				return False
			raise e
		return True
