import convert_json_to_url_list
import kyodo_RSS
import runspider
import search_key_from_article


def clear_cash(cash_path_list: list):
    for path in cash_path_list:
        with open(path, mode='w') as f:
            f.write("")


RSS_setting_path = "RSS_setting.yml"
path_result = "kyodo_articles/data/results.json"
include_out_path = "URL_list_keyword_include.txt"
key_words_not_include = "./kyodo_articles/data/key_words_not_include.json"
start_url = "starts_urls.txt"
cash_list = [path_result, start_url,key_words_not_include]

kyodo_RSS.main(RSS_setting_path)
convert_json_to_url_list.main()
runspider.main()
search_key_from_article.main()
clear_cash(cash_list)
print("Scraping was complete!!!")
