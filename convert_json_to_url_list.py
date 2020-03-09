# -*- coding: utf-8 -*-
import json


def main(origin_json_path_main: str = "./kyodo_articles/data/key_words_not_include.json",
         export_path_dir: str = "starts_urls.txt"):
    json_data = load_json(origin_json_path_main)
    write_url_list(json_data, export_path_dir)


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_url_list(json_data: dict, export_path: str):
    export_list = [str(x["url"]) + '\n' for x in json_data]
    with open(export_path, 'a') as f:
        f.writelines(export_list)


if __name__ == "__main__":
    origin_json_path = "./kyodo_articles/data/not_target_entres.json"
    export_path_file_main = "starts_urls.txt"
    main(origin_json_path, export_path_file_main)
