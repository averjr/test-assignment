import asyncio
import sys
import tempfile
import zipfile
from os import listdir
from os.path import isfile, join

import requests
import validators
from requests.exceptions import RequestException
from zipfile import BadZipFile
from aiobotocore.session import get_session
from typing import Generator
import _io


BUCKET = 'for-wg-test'  # TODO: make it configurable or create a bucket if not exists


class WrongUrlException(Exception):
    pass


async def main(url: str) -> None:
    tmp_zip_file = download_file(url)

    session = get_session()
    async with session.create_client("s3") as client:
        res = await asyncio.gather(*[upload(client, file) for file in get_zipped_files(tmp_zip_file)])
    print(f"Uploading finished: {len(res)}")


async def upload(client, file: str) -> None:  # What is the right type for client?
    filename = file.split("/")[-1]
    try:
        with open(file, 'rb') as f:
            print(f"Start uploading file {filename}")
            await client.put_object(Bucket=BUCKET, Key=filename, Body=f.read())
    except Exception as e:
        print(f"There is error on uploading file {filename}")
        print(e)
    else:
        print(f"This file uploaded successfully: {filename}")


def get_zipped_files(tmp_zip_file: _io.BufferedRandom) -> Generator[str, None, None]:
    print(f"Start unzip files")
    dirpath = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(tmp_zip_file, "r") as zip_fh:
            zip_fh.extractall(dirpath)
    except BadZipFile:
        print("Broken zip file")
    else:
        print(f"Unzipped successfully")
        for file in listdir(dirpath):
            full_path = join(dirpath, file)
            if isfile(full_path):
                yield full_path


def download_file(url: str) -> _io.BufferedRandom:
    print(f"Start file downloading from: {url}")
    try:
        tmp_file = tempfile.TemporaryFile()
        with requests.get(url, allow_redirects=True) as r:
            r.raise_for_status()
            tmp_file.write(r.content)
        print(f"File downloaded successfully")
        return tmp_file
    except RequestException:
        print("Wrong url or connection error")


def init(*args):
    try:
        url = sys.argv[1]
        if not validators.url(url):
            raise WrongUrlException("Use proper url to zip file")
        asyncio.run(main(url))
    except IndexError:
        print("Please pass proper url as argument")
    except Exception as e:
        print(e)
    # TODO: add --help
    # TODO: add --t --threads for threading approach


if __name__ == "__main__":
    init()
# TODO: use logger not print
# TODO: Use separate file for texts
