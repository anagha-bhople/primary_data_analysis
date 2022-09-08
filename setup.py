from setuptools import setup


REQUIREMENTS = ['numpy','pandas','matplotlib','six','plotly',
'statsmodels','seaborn','sklearn', 'setuptools']

# calling the setup function
setup(name='primarydataanalysis',
	version='1.0.0',
	description='Primary data analysis for pandas dataframe',
	long_description='Primary data analysis for pandas dataframe',
	url='https://github.com/anagha-bhople/primary_data_analysis',
	author='Anagha Bhople',
	author_email='bhoplea34@gmail.com',
	license='MIT',
	install_requires=REQUIREMENTS,
	keywords='data analysis eda pandas'
	)
