import os
import logging
import re

import boto3
import ebcli.core.fileoperations as fileoperations
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def replace_docker_images():
    image_replacements = json.loads(os.environ['INPUT_CONTAINER_IMAGES'])

    with open('Dockerrun.aws.json') as f:
        data = json.load(f)
        for container_definition in data['containerDefinitions']:
            name = container_definition['name']
            if name in image_replacements.keys():
                container_definition['image'] = image_replacements[name]
        updated = json.dumps(data, indent=4, sort_keys=True)

    with open('Dockerrun.aws.json', 'w') as f:
        f.write(updated)


def build_bundle(file_name):
    file_path = fileoperations.get_zip_location(file_name)
    logging.info('Packaging application to %s', file_path)
    ignore_files = fileoperations.get_ebignore_list()
    fileoperations.io.log_info = lambda message: logging.debug(message)
    fileoperations.zip_up_project(file_path, ignore_list=ignore_files)


def build_version_label():
    app = os.environ['INPUT_APP']
    ref = os.environ['GITHUB_REF']

    ref_no_prefix = re.sub('^refs/(heads/)?', '', ref)
    ref_no_suffix = re.sub('/head$', '', ref_no_prefix)
    ref_special_as_underscore = re.sub('[-/]', '_', ref_no_suffix)

    clean_branch_name = ref_special_as_underscore

    build_number = os.environ['GITHUB_RUN_ID']
    git_sha = os.environ['GITHUB_SHA']
    return "{}-{}-{}-{}".format(app, clean_branch_name, build_number, git_sha)


def upload_bundle(file_name, bucket, app_version):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, app_version)


def build_description():
    return "description"


def create_app_version(app, version_label, bucket, key):
    elasticbeanstalk = boto3.client('elasticbeanstalk')
    elasticbeanstalk.create_application_version(
        app,
        version_label,
        build_description(),
        SourceBundle={
            'S3Bucket': bucket,
            'S3Key': key
        }
    )


def main():
    replace_docker_images()
    version_label = build_version_label()
    file_name = "{}.zip".format(version_label)
    build_bundle(file_name)

    app = os.environ['INPUT_APP']
    bucket = os.environ['INPUT_S3_BUCKET']
    key = '{}/{}.zip'.format(app, file_name)

    upload_bundle(file_name, bucket, key)
    create_app_version(app, version_label, bucket, key)


if __name__ == "__main__":
    main()
