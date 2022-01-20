import aiobotocore
from aiobotocore.config import AioConfig
import os
import pytest


_PYCHARM_HOSTED = os.environ.get('PYCHARM_HOSTED') == '1'


@pytest.fixture
def s3_verify():
    return None


@pytest.fixture
def session():
    session = aiobotocore.session.AioSession()
    return session


@pytest.fixture
def region():
    return 'us-east-1'


@pytest.fixture
def signature_version():
    return 's3'


@pytest.fixture
def mocking_test():
    # change this flag for test with real aws
    # TODO: this should be merged with pytest.mark.moto
    return True


@pytest.fixture
def config(region, signature_version):
    connect_timeout = read_timout = 5
    if _PYCHARM_HOSTED:
        connect_timeout = read_timout = 180

    return AioConfig(region_name=region, signature_version=signature_version,
                     read_timeout=read_timout, connect_timeout=connect_timeout)


@pytest.fixture
async def s3_client(session, region, config, s3_server, mocking_test, s3_verify):
    kw = moto_config(s3_server) if mocking_test else {}

    async with session.create_client('s3', region_name=region,
                                     config=config, verify=s3_verify, **kw) as client:
        yield client


def moto_config(endpoint_url):
    kw = dict(endpoint_url=endpoint_url,
              aws_secret_access_key="xxx",
              aws_access_key_id="xxx")

    return kw


pytest_plugins = ['tests.mock_server']
