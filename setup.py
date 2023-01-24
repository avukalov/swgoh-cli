from setuptools import setup

setup(
    name='swgoh',
    version='0.1.0',
    packages=[
        'swgoh',
        'swgoh.apis',
        'swgoh.classes',
        'swgoh.commands',
        'swgoh.models',
        'swgoh.tests',
        'swgoh.utils',
    ],
    # scripts=['capitalize/bin/cap_script.py'],
    # package_data={'capitalize': ['data/cap_data.txt']}
    install_requires=[
        'Click',
        'swgoh_comlink',
        'python-dotenv',
        'redis'
    ],
    entry_points={
        'console_scripts': [
            'swgoh = swgoh.swgoh:cli',
        ],
    },
)