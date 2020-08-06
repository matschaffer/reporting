import os
import logging
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


def build_filename():
    app = os.environ['INPUT_APP']
    ref = os.environ['GITHUB_REF']
    clean_branch_name = ref.replace('refs/', '').replace('heads/', '').replace('/', '_')
    build_number = os.environ['GITHUB_RUN_ID']
    git_sha = os.environ['GITHUB_SHA']
    return "{}-{}-{}-{}.zip".format(app, clean_branch_name, build_number, git_sha)


def upload_bundle(file_name):
    bucket = os.environ['INPUT_S3_BUCKET']
    pass


def main():
    replace_docker_images()
    file_name = build_filename()
    build_bundle(file_name)
    upload_bundle(file_name)


if __name__ == "__main__":
    main()
