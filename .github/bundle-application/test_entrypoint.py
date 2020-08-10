import json
import os

import boto3
import pytest
from moto import mock_s3, mock_elasticbeanstalk

import entrypoint

app = 'pytest'
version_label = 'pytest-master-123abcdef456'
bucket = 'test-bucket'


def test_replace_docker_images(tmpdir):
    with tmpdir.as_cwd():
        with open('Dockerrun.aws.json', 'w') as f:
            json.dump({"containerDefinitions": [
                {"name": "proxy", "image": "original_image"},
                {"name": "grafana", "image": "original_image"},
            ]}, f)

        os.environ['INPUT_CONTAINER_IMAGES'] = json.dumps({"grafana": "updated_image"})
        entrypoint.replace_docker_images()

        with open('Dockerrun.aws.json') as f:
            data = json.load(f)
            assert [c['image'] for c in data['containerDefinitions'] if c['name'] == 'grafana'] == ['updated_image']


def test_build_bundle(tmpdir):
    with tmpdir.as_cwd():
        path = entrypoint.build_bundle(version_label)
        assert path == '.elasticbeanstalk/app_versions/{}.zip'.format(version_label)
        assert os.path.exists(path)


def test_build_version_label():
    os.environ['INPUT_APP'] = 'unittest'
    os.environ['GITHUB_RUN_ID'] = '8675309'
    os.environ['GITHUB_SHA'] = '0123456789abcdef'

    os.environ['GITHUB_REF'] = 'refs/heads/master'
    assert entrypoint.build_version_label() == 'unittest-master-8675309-0123456789abcdef'

    os.environ['GITHUB_REF'] = 'refs/pull/5/head'
    assert entrypoint.build_version_label() == 'unittest-pull_5-8675309-0123456789abcdef'

    os.environ['GITHUB_REF'] = 'refs/heads/tiles-tf'
    assert entrypoint.build_version_label() == 'unittest-tiles_tf-8675309-0123456789abcdef'


def test_build_description():
    os.environ['GITHUB_SERVER_URL'] = 'https://github.com'
    os.environ['GITHUB_REPOSITORY'] = 'Safecast/reporting2'
    os.environ['GITHUB_RUN_ID'] = '198909110'
    assert entrypoint.build_description() == 'github.com/Safecast/reporting2/actions/runs/198909110'


@mock_s3
def test_upload_bundle(tmpdir):
    with tmpdir.as_cwd():
        # noinspection PyUnresolvedReferences
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=bucket)

        path = entrypoint.build_bundle(version_label)
        key = entrypoint.upload_bundle(path, bucket, 'pytest')
        assert key == 'pytest/{}.zip'.format(version_label)


@pytest.mark.skip(reason="moto doesn't yet implement create_application_version")
@mock_elasticbeanstalk
def test_create_app_version(tmpdir):
    with tmpdir.as_cwd():
        # entrypoint.create_app_version(app, version_label, bucket, key)
        pass
