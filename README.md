# test-assignment

This util's purpose is to:
 1. download zip file from given url
 2. unpack zip
 3. upload files to S3

Assuming you've got configured AWS credentials, there should be
```
~/.aws/config
```
and
```
~/.aws/credentials
```
files with proper content.

You will also need to create S3 Bucket with name ***'for-wg-test'***

To run tests:
```
$ python setup.py test
```
To install cli:
```
$ python setup.py install
```
After setup.py install you can use utils from command line as
```
$ zips3uploader https://github.com/averjr/test-assignment/raw/main/files.zip
```
