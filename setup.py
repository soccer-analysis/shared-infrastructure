import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

with open('Pipfile', 'r') as pf:
	install_requires = [
		x.split('=')[0].strip()
		for x in pf.read().split('[packages]')[-1].split('[')[0].strip().splitlines()
	]


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
	install_requires=install_requires,
)
