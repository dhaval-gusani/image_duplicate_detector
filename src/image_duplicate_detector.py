import os
import argparse
import hashlib
import base64

SEPARATOR = os.sep
BASE_DIRECTORY = ''
HASH_INDEX = {}
DUPLICATES = []


def _parse_arguments_():
    """
    Parses command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-bd', '--base_directory', help='Directory path for image source base',
                        action='store', required=True)
    return parser.parse_args()


def _get_content_of_file(file):
    with open(file, "rb") as imageFile:
        return base64.b64encode(imageFile.read())


def _add_to_index(hash, file_path):
    if hash in HASH_INDEX:
        HASH_INDEX[hash].append(file_path)
    else:
        HASH_INDEX[hash] = [file_path]


def _get_hash_(content):
    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest()


def _create_index():
    for dir_path, directory_names, file_names in os.walk(BASE_DIRECTORY):
        for file in file_names:
            file_path = dir_path + SEPARATOR + file
            _add_to_index(_get_hash_(_get_content_of_file(file_path)), file_path)


def _detect_duplicates(file_path, same_hash_files, content):
    remaining_same_hash_files = list(set(same_hash_files) - set([file_path]))
    for index_file in remaining_same_hash_files:
        if content == _get_content_of_file(index_file):
            key = _get_key_of_2_paths(file_path, index_file)
            if key not in DUPLICATES:
                DUPLICATES.append(key)
                print('Detected Duplicates: ' + index_file + " - " + file_path)


def _get_key_of_2_paths(file_path, index_file):
    duplicate_entry = [index_file, file_path]
    duplicate_entry.sort()
    key = ""
    for entry in duplicate_entry:
        key = key + entry

    return key


def _process_():
    _create_index()
    for dir_path, directory_names, file_names in os.walk(BASE_DIRECTORY):
        for file in file_names:
            file_path = dir_path + SEPARATOR + file
            content = _get_content_of_file(file_path)
            same_hash_files = HASH_INDEX[_get_hash_(content)]
            _detect_duplicates(file_path, same_hash_files, content)


if __name__ == '__main__':
    args = _parse_arguments_()
    BASE_DIRECTORY = args.base_directory
    _process_()