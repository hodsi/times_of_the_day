import json
import os


def safe_join_path(path: str, *paths: str):
    joined_path = path
    for path_to_join in paths:
        if not os.path.isdir(joined_path):
            os.mkdir(joined_path)
        joined_path = os.path.join(joined_path, path_to_join)
    return joined_path


def dump_json_to_file(list_to_dump, file_path):
    with open(file_path, 'w') as f:
        json.dump(list_to_dump, f)
