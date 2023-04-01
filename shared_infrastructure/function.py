from dataclasses import dataclass
from os import getcwd
from typing import cast, Dict, List

from aws_cdk import Duration
from aws_cdk.aws_ecr_assets import Platform
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, Function
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct


@dataclass
class Allow:
	actions: List[str]
	resources: List[str]


def create_function(scope: Construct, name: str, cmd: str, env: Dict[str, str],
					allows: List[Allow], memory_size: int = 512,
					reserved_concurrent_executions: int = 1) -> Function:
	return DockerImageFunction(
		scope,
		f'{name}-function',
		function_name=name,
		reserved_concurrent_executions=reserved_concurrent_executions,
		memory_size=memory_size,
		timeout=Duration.minutes(15),
		log_retention=RetentionDays.FIVE_DAYS,
		code=DockerImageCode.from_image_asset(
			directory=getcwd(),
			platform=cast(Platform, Platform.LINUX_AMD64),
			file='Dockerfile',
			cmd=[cmd]
		),
		environment=env,
		role=Role(
			scope,
			f'{name}-role',
			assumed_by=ServicePrincipal('lambda.amazonaws.com'),
			managed_policies=[ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')],
			inline_policies={
				'Policies': PolicyDocument(statements=[
					PolicyStatement(
						effect=Effect.ALLOW,
						actions=allow.actions,
						resources=allow.resources
					)
					for allow in allows
				])
			}
		)
	)
