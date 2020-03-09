#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 共同通信のRSSから新着分のデータを取得し,キーワードファイルから記事見出しもしくは本文にキーワードが存在するかをチェック
# 存在したらJSONでURLと記事と見出しを吐き出す
import json
import sys

import feedparser
import pandas as pd
import yaml


def main(setting_path: str):
    # 設定ファイルの読み込み
    config = import_setting(setting_path)

    # 現在のRSからデータを取得
    rss_url = config["RSS_URL"]
    new_data = get_rss_data(rss_url)

    # 過去全エントリーリストを読み込み
    old_data_path = config["older_entry_list"]
    old_data = import_old_data(old_data_path)

    # 新着のエントリーが存在するかチェック
    diff_data = check_new_entry(new_data, old_data)
    if diff_data is None:
        # 新着のエントリーが存在しなかったとき処理を終了
        return

    # 全エントリーリストに新着リストを保存
    save_rss(diff_data, config["older_entry_list"])

    # タイトルに含まれているかどうか調べるキーワードリスト読み込み
    keywords_list = import_keywords_list(config["key_word_list"])
    new_target = search_keywords_from_key(keywords_list, diff_data)

    # 新着のエントリーの中からタイトルに含まれているURLをキーワードがURLリストとして保存
    save_rss(new_target, config["target_entry_list"])
    print("========================================================")
    # 新着のエントリーの中からタイトルにキーワードが含まれて"いない"URLリストとして保存
    others_data = check_new_entry(diff_data, new_target)
    save_rss(others_data, config["not_target_entry_list"])


def get_rss_data(feed_url: str):
    """

    :param feed_url: データを調べるRSSのURL
    :return: RSSからURLとタイトルを抜き出したデータをpandsの表に変換したものを返す
    """
    # URLから取得したデータをpandasのDataframeに変換
    kyodo_rss_data = feedparser.parse(feed_url)
    df = [{'url': e['link'], 'title': e['title']} for e in kyodo_rss_data['entries']]
    return pd.json_normalize(df)


def import_old_data(path: str):
    # jsonを読み込んでpandasのdataframeに変換
    with open(path, 'ab+') as f:  # ファイルを開く
        if f.tell() == 0:  # ファイルが空かチェック
            df = pd.DataFrame(columns=["url", "title"])
            tmp = pd.Series([0, 0], index=df.columns)
            df = df.append(tmp, ignore_index=True)
            return df
        else:
            return pd.read_json(path)


def dict_in_list_change_to_df(data):
    return pd.json_normalize(data)


def check_new_entry(new_data, old_data):
    """

    :param new_data: データが次のold_dataと重複している部分があるか調べる
    :param old_data:
    :return: データで重複していない部分のみ返す
    """
    # new_dataにold_dataと一致する行が存在するか調べる
    if new_data.empty is False:
        new_data["比較用の列"] = new_data[["url", "title"]].apply(lambda x: "{}_{}".format(x[0], x[1]), axis=1)
    else:
        new_data = {}
    if old_data.empty is False:
        old_data["比較用の列"] = old_data[["url", "title"]].apply(lambda x: "{}_{}".format(x[0], x[1]), axis=1)
        # new_dataにのみ存在する行を表示
        df_diff = new_data[~new_data['比較用の列'].isin(old_data['比較用の列'])]
    else:
        df_diff = pd.DataFrame()
        print("hi")
    if df_diff.empty:
        print("新着のニュースはありません")
        sys.exit(1)
    else:
        print("差分表示")
        print(df_diff)
    return df_diff


def import_keywords_list(path: str) -> list:
    # タイトルで検索するキーワードリストを読み込み
    with open(path, encoding="utf-8") as f:
        word_list = f.read().splitlines()
        # 空行削除
        word_list = [a for a in word_list if a != '']
        # 半角スペース削除
        word_list = [a.replace(" ", "") for a in word_list]
        # 全角スペース削除
        word_list = [a.replace("　", "") for a in word_list]
    return word_list


def search_keywords_from_key(key_words: list, data_df, dict_key: str = "title"):
    """

    :param key_words:検索語のリスト
    :param data_df:検索するデータ全体(pandasのDataFrame)
    :param dict_key: 検索するデータの行の名前
    :return:
    """
    # data_dfのtitle列にkey_wardに含まれた文字列が存在するかチェック
    out_df = pd.DataFrame()
    for search_word in key_words:
        tmp_df = data_df[data_df[dict_key].str.contains(search_word)]
        if tmp_df.empty:
            print("ないです")
        else:
            print("{keywords}はあります".format(keywords=search_word))
            print(tmp_df)
            out_df = out_df.append(tmp_df)
    return out_df


def import_setting(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        config = yaml.safe_load(f.read())
    return config


def append_json_to_file(data: dict, path_file: str) -> bool:
    # 備考https://qiita.com/KEINOS/items/ea4bda15506bbd3e6913
    with open(path_file, 'ab+') as f:  # ファイルを開く
        f.seek(0, 2)  # ファイルの末尾（2）に移動（フォフセット0）
        if f.tell() == 0:  # ファイルが空かチェック
            # if
            # 空の場合は JSON 配列を書き込む data自体がリストなので[data]ではなくdataに変更する
            f.write(json.dumps(data, ensure_ascii=False, indent=2).encode())
        else:
            f.seek(-1, 2)  # ファイルの末尾（2）から -1 文字移動
            f.truncate()  # 最後の文字を削除し、JSON 配列を開ける（]の削除）
            for data_line in data:
                f.write(',\n'.encode())  # 配列のセパレーターを書き込む
                f.write(json.dumps(data_line, ensure_ascii=False, indent=4).encode())  # 辞書を JSON 形式でダンプ書き込み
            f.write(']'.encode())  # JSON 配列を閉じる
    return f.close()  # 連続で追加する場合は都度 Open, Close しない方がいいかも


def save_rss(data, path: str):
    if data.empty is True:
        save_data = {}

    else:
        save_data = data.loc[:, ["url", "title"]].to_dict(orient='records')
    append_json_to_file(save_data, path)
    return


if __name__ == '__main__':
    setting_file_path = "RSS_setting.yml"
    main(setting_file_path)
# main("RSS_setting.yml")
