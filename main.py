from sys import stdin
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import Crawler_module
import Scraper_module
import json
import os


def main():
    with open('DSL_setting_file2.json',encoding="utf-8") as f:
    #jsonファイルを辞書型として取得
        DSL = json.load(f)
    #始点となるURLを入力とする
    url1 = DSL['clawler']['開始URL']
    #抽出したい箇所のCSSセレクタを入力とする
    selector_crawler = DSL['clawler']['リンク抽出セレクタ']
    #変数dataにスクレイパーへ渡す値を入れる
    data = DSL['scraper']
    new_dir_path = input("フォルダを作成するパスを入力してください>>>")
    try:
        #raw文字列でエスケープシーケンスを無視する
        new_dir_path = r'{0}\{1}'.format(new_dir_path,data['大学名'])
        os.mkdir(new_dir_path)
    except:
        print("このディレクトリはすでに作成されています")

    crawl_function = Crawler_module.crawler(url1,selector_crawler)
    for url2 in crawl_function:
        scraping_function = Scraper_module.scraper(url2,data)
        #辞書型であるkougi_dataをjson形式で取得する。ファイル名はkougi_data['5'](履修コード)にする
        with open(r'{0}\{1}.json'.format(new_dir_path,scraping_function['id']),'w',encoding="utf-8") as f:
            json.dump(scraping_function,f,ensure_ascii=False)
main()
