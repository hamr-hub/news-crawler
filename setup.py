from setuptools import setup, find_packages

setup(
    name='news_crawler',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Scrapy',
        'scrapy-playwright',
        'redis',
        'scrapy-redis',
        'openai',
        'pydantic',
    ],
)
