import setuptools
from dparse import parse, filetypes

with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

with open('Pipfile', 'r') as pf:
	pipfile = parse(pf, file_type=filetypes.pipfile)

setuptools.setup(
	name='shared-infrastructure',
	version='0.0.1',
	author='Aaron Mamparo',
	author_email='aaronmamparo@gmail.com',
	description='Shared infrastructure for the soccer-analysis project',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/soccer-analysis/shared-infrastructure',
	project_urls={
		"Bug Tracker": "https://github.com/soccer-analysis/shared-infrastructure/issues"
	},
	license='MIT',
	packages=['shared_infrastructure'],
	install_requires=[x.name for x in pipfile.dependencies if x.section == 'packages'],
)
