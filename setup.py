import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='gd_analysis',
    description='Goal Difference Analysis Project',
    version='0.0.1',
    author='Sebastian Schneider',
    author_email='sebastian.schneider01@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sebschneid/gd-analysis',
    packages=setuptools.find_packages(),
    package_data={
        'gd_analysis': [
            'data/df_datasets.pkl',
            'data/df_players.pkl',
            'data/df_matches.pkl',
        ]
    },
)
