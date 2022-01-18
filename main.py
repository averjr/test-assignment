import asyncio
import re
import sys
import tempfile
import zipfile
from os import listdir
from os.path import isfile, join

import aioboto3
import aiofiles
import requests
import validators
from requests.exceptions import RequestException


BUCKET = 'for-wg-test'


class WrongUrlException(Exception):
    pass


# TODO: upload files to S3
# TODO: Process multipart
async def write_files_to_s3(dirpath):
    files = [join(dirpath, f) for f in listdir(dirpath) if isfile(join(dirpath, f))]

    session = aioboto3.Session()
    async with session.client("s3") as s3:
        for file in files:
            async with aiofiles.open(file, mode="rb") as fpr:
                await s3.upload_fileobj(fpr, BUCKET, file.split("/")[-1])


# TODO: unzip recursively
def unzip_file(path):
    dirpath = tempfile.mkdtemp()
    with zipfile.ZipFile(path, "r") as zip_fh:
        zip_fh.extractall(dirpath)
    return dirpath


def write_file(bytes):
    f = tempfile.TemporaryFile()
    f.write(bytes)
    return f


# TODO: download file
def download_file(url):
    try:
        # TODO: handle 404
        with requests.get(url, allow_redirects=True) as r:
            filename = ""
            if "Content-Disposition" in r.headers.keys():
                filename = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            else:
                filename = url.split("/")[-1]  # TODO: use urllib.parse.unquote to avoid "%20" in filenames
            return r.content
    except RequestException as e:
        print(e)


if __name__ == '__main__':
    try:
        # TODO: Parse parameter
        url = sys.argv[1]
        if not validators.url(url):
            raise WrongUrlException("Use proper url to zip file")
        bytes = download_file(url)
        fh = write_file(bytes)
        folder_with_files = unzip_file(fh)
        asyncio.run(write_files_to_s3(folder_with_files))

    except IndexError:
        raise Exception("Please pass url to zip file")
    # TODO: add --help


# TODO: Add tests
# TODO: Add setup.py
# TODO: Write Readme
# TODO: Set AWS env vars
# TODO: Be verbose use ProcessPercentage
