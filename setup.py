from setuptools import setup

setup(
    name='represent-maps',
    packages=['maps', 'maps.management', 'maps.management.commands'],
    version='0.1',
    install_requires=[
        'django-appconf',
        'django-jsonfield>=0.7.1'
    ],
)