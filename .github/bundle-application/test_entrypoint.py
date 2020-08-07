import json
import os
import entrypoint


def test_image_replacement(tmpdir):
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
        os.makedirs('.elasticbeanstalk')
        entrypoint.build_bundle('blah.zip')
        assert os.path.exists('.elasticbeanstalk/app_versions/blah.zip')


def test_bundle_naming():
    os.environ['INPUT_APP'] = 'unittest'
    os.environ['GITHUB_RUN_ID'] = '8675309'
    os.environ['GITHUB_SHA'] = '0123456789abcdef'

    os.environ['GITHUB_REF'] = 'refs/heads/master'
    assert entrypoint.build_version_label() == 'unittest-master-8675309-0123456789abcdef'

    os.environ['GITHUB_REF'] = 'refs/pull/5/head'
    assert entrypoint.build_version_label() == 'unittest-pull_5-8675309-0123456789abcdef'

    os.environ['GITHUB_REF'] = 'refs/heads/tiles-tf'
    assert entrypoint.build_version_label() == 'unittest-tiles_tf-8675309-0123456789abcdef'

