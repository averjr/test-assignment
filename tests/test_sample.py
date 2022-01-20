from zips3uploader.zips3uploader import download_file, get_zipped_files, upload, BUCKET
from tests.fixtures import ZIP_FILE, ZIP_FILE_BROKEN
from io import BufferedRandom, BytesIO
import pytest


class TestClass:
    def test_download_file(self, requests_mock):
        url = 'http://localhost'
        requests_mock.get(url, content=ZIP_FILE)
        result = download_file(url)
        assert type(result) == BufferedRandom
        assert result.__sizeof__() == 4248

    def test_download_file_404(self, requests_mock, capsys):
        url = 'http://localhost'
        requests_mock.get(url, status_code=404)
        download_file(url)
        captured = capsys.readouterr()
        assert "Wrong url or connection error" in captured.out

    def test_get_zipped_files(self, capsys):
        files = list(get_zipped_files(BytesIO(ZIP_FILE)))
        captured = capsys.readouterr()
        for file in files:
            assert file.split("/")[-1] in ['file2.txt', 'file1.txt']
        assert "Unzipped successfully" in captured.out

    def test_get_zipped_files_broken_file(self, capsys):
        list(get_zipped_files(BytesIO(ZIP_FILE_BROKEN)))
        captured = capsys.readouterr()
        assert "Broken zip file" in captured.out

    @pytest.mark.asyncio
    async def test_upload(self, s3_client):
        await s3_client.create_bucket(Bucket=BUCKET)
        files = list(get_zipped_files(BytesIO(ZIP_FILE)))
        for file in files:
            await upload(s3_client, file)

        res = await s3_client.list_objects_v2(Bucket=BUCKET)

        files_name_from_s3 = [f['Key'] for f in res.get('Contents')]
        files_name_for_upload = [f.split("/")[-1] for f in files]

        assert sorted(files_name_from_s3) == sorted(files_name_for_upload)
