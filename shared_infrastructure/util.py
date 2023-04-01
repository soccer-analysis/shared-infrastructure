import boto3


def get_stack_output(stack_name: str, export_name: str) -> str:
	stack = boto3.resource('cloudformation').Stack(stack_name)
	output = next(x for x in stack.outputs if x['ExportName'] == export_name)
	if not output:
		raise f'Output with export name "{export_name}" not found in "{stack_name}'
	return output['OutputValue']
