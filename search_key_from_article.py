import json

import pandas as pd


def main():
    data_path = "./kyodo_articles/data/results.json"
    keyword_list_path = "key_word_list.txt"
    search_target_dict_keys = ["text", "label", "url"]
    include_out_path = "URL_list_keyword_include.txt"
    not_include_out_path = "URL_list_keyword_not_include.txt"
    # 　jsonのデータを読み込んでデータ内にある目的のリストをテキストに変換
    # textならその記事のテキスト自体がリスト形式になっている
    data = import_json_data_to_dict(data_path, search_target_dict_keys)

    # 辞書のデータをpandsの表に
    df = pd.json_normalize(data)
    # 記事内から検索するキーワードのリストを読み込み
    key_word_list = import_keywords_list(keyword_list_path)

    save_include_dict, save_not_include_dict = search_keywords_from_key_list(key_word_list, df, search_target_dict_keys)
    print("hi")

    # URLリストとして保存
    export_url_list(save_include_dict, include_out_path)
    export_url_list(save_not_include_dict, not_include_out_path)
    print("end")


def import_json_data_to_dict(data_path: str, search_targets: list):
    # jsonのデータを読み込みこんでリスト内包辞書内包リストを辞書内包リストに変換
    # 記事の本文などがリストになっているのを解除
    with open(data_path, "r", errors='ignore', encoding="utf-8") as f:
        data = json.load(f)
        for i in range(len(data)):  # enumerate()だと動かないがなぜかrange(len())だと動く
            for dict_key in search_targets:
                # 読み込んだデータがリストになっているので結合
                data[i][dict_key] = "".join(data[i][dict_key])
        return data


def import_keywords_list(keyword_list_path: str) -> list:
    # タイトルで検索するキーワードリストを読み込み
    with open(keyword_list_path, encoding="utf-8") as f:
        word_list = f.read().splitlines()
        # 空行削除
        word_list = [a for a in word_list if a != '']
        # 半角スペース削除
        word_list = [a.replace(" ", "") for a in word_list]
        # 全角スペース削除
        word_list = [a.replace("　", "") for a in word_list]
    return word_list


def search_keywords_from_key_list(search_targets: list, search_target_data, dict_key_list):
    # 検索する"単語のリスト"から目的の単語が記事に含まれていないか検索
    """

    :param search_targets:検索をかけるキーワード(検索語)
    :param search_target_data: 検索する先のデータ
    :param dict_key_list: 検索するデータが格納されている行の名前リスト(カラム名のリスト)
    :return:キーワードを含んだデータ,キーワードを含んでいないデータ で返す(dict)
    """
    out = pd.DataFrame()
    key_words_included = pd.DataFrame()
    key_words_not_included = pd.DataFrame()

    tmp = pd.DataFrame()
    for dict_key in dict_key_list:
        # 検索する項目でループ(タイトルとラベルでループ)
        tmp = search_keywords_from_key(search_targets, search_target_data, dict_key)
        out = pd.concat([out, tmp])
    print("hi")
    out = out.drop_duplicates()
    key_words_included = out.to_dict(orient="records")
    # キーワードを含んでいないリストを作成
    out2 = check_new_entry(search_target_data, out, dict_key_list)
    key_words_not_included = out2.to_dict(orient="records")
    return key_words_included, key_words_not_included


def search_keywords_from_key(key_words: list, data_df, search_target_dict_key: str):
    # 検索する単語が
    # data_dfのtitle列にkey_wardに含まれた文字列が存在するかチェック
    """

    :param key_words: 検索をかけるワード(検索語)
    :param data_df: 検索するデータ全体
    :param search_target_dict_key:検索する行の名前
    :return:
    """
    out_df = pd.DataFrame()
    for search_word in key_words:
        # key_wordsがリストになっているのでstrに変換
        tmp_df = data_df[data_df[search_target_dict_key].str.contains(search_word)]
        if tmp_df.empty:
            print("ないです")
        else:
            print(
                "{keywords}は{search_target_dict_key}にありました".format(
                    keywords=key_words, search_target_dict_key=search_target_dict_key))
            # print(tmp_df)
            out_df = out_df.append(tmp_df)
    return out_df


def check_new_entry(new_data, old_data, dict_list):
    """
    newdataとold_dataの差集合 (new_data - old_data もしくはnew_data ∖ old_data)をpandsのDataFrame形式で返す
    :param new_data: 比較元
    :param old_data: 減算元
    :param dict_list:辞書のキー
    :return:
    """
    # new_dataにold_dataと一致する行が存在するか調べる
    new_data["比較用の列"] = new_data[dict_list].apply(lambda x: "{}_{}".format(x[0], x[1]), axis=1)
    old_data["比較用の列"] = old_data[dict_list].apply(lambda x: "{}_{}".format(x[0], x[1]), axis=1)
    # new_dataにのみ存在する行を表示
    df_diff = new_data[~new_data['比較用の列'].isin(old_data['比較用の列'])]
    if df_diff.empty:
        return pd.DataFrame()
    else:
        return df_diff


def export_url_list(json_data: dict, export_path: str):
    export_list = [str(x["url"]) + '\n' for x in json_data]
    with open(export_path, 'a+') as f:
        f.writelines(export_list)
    return


if __name__ == '__main__':
    main()
