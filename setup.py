from setuptools import setup, find_packages

setup(
    name='zips3uploader',
    version='0.0.1',
    description='Download .zip given by url and upload files from it to S3',
    author='Andrii Averkiiev',
    author_email='averkiev.jr@gmail.com',
    packages=find_packages(include=['zips3uploader', 'zips3uploader.*']),
    install_requires=[
        'validators==0.18.2',
        'requests==2.27.1',
        'aioboto3==9.3.1',
        'aiobotocore==2.1.0',
        'aiofiles==0.8.0',
        'aiohttp==3.8.1',
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=[
        'pytest==6.2.5',
        'requests-mock==1.9.3',
        'moto==2.3.2',
        'pytest-asyncio==0.17.2',
        'nest-asyncio==1.5.4',
        'Flask==2.0.2',
        'Flask-Cors==3.0.10',
        'aiohttp==3.8.1',
    ],
    entry_points={
        'console_scripts': ['zips3uploader=zips3uploader.zips3uploader:init']
    }
)
