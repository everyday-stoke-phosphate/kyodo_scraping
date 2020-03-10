Python3.7以上で(開発環境は3.8)  
必要なパッケージ
- scrapy
- pandas
- pyyaml
- feedparser

windowsはscrapyをインストールするときVisual C++のコンパイラが必要なので注意  
ダウンロード  
https://visualstudio.microsoft.com/ja/downloads/  
Build Tools for Visual Studioを選んでダウンロード  
windowsはstart_scraping.batをタスクスケジューラーに  
linuxはstart_scraping.bashをcronに  
それぞれ登録してください  

Macのやり方はここに  
解説を書いて頂けました  
https://hackmd.io/@covid19-kenmo/kyodo-scaraping#%E5%85%B1%E5%90%8C%E9%80%9A%E4%BF%A1%E3%81%AE%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88  
RSSは最大で50件までしかニュースを保持しないので実行間隔を開けすぎると回収漏れが出てきます  
15分程度を目安に今のところ運用しています  
検索したキーワードが含まれているデータはURL_list_keyword_include.txtに保存されます    
一方含まれていないデータはURL_list_keyword_not_include.txtに保存されています  
(今後RSS_setting.ymlの設定を変えるだけで保存先などを変えられるようにする予定)

ライセンスはMITで
