共同通信の記事(this.kiji.is)をRSSから取得し、指定のキーワードが見出し、本文、関連ワード(記事作成者がつける分類わけのタグ)に含まれていないか探してくるスクリプトです。  
このスクリプトは動き出した時より前は基本的にデータを集められません。動かしたときから配信された記事の中に指定のキーワードが存在するか調べ、その記事のURLリストを作成するスクリプトです。

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
https://hackmd.io/@covid19-kenmo/kyodo-scraping
RSSは最大で50件までしかニュースを保持しないので実行間隔を開けすぎると回収漏れが出てきます  
15分程度を目安に今のところ運用しています  
検索したキーワードが含まれているデータはURL_list_keyword_include.txtに保存されます    
一方含まれていないデータはURL_list_keyword_not_include.txtに保存されています  
(今後RSS_setting.ymlの設定を変えるだけで保存先などを変えられるようにする予定)

ライセンスはMITで
