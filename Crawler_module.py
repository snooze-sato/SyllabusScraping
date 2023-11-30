import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time

s=0
def crawler(url,selector):

    while True:
        try:
            #URLのHTML文書をresponse型で取得する
            time.sleep(1)
            response = requests.get(url)
            break
        #対象サーバーからのレスポンスがない場合,処理を一時停止させる
        except:

            print("********************************\n\
            ********************************\n\
            ********************************\n\
            Pause10000ms\n\
            ********************************\n\
            ********************************\n\
            ********************************\n\
            ")
            time.sleep(10)

    #html.parserとlxmlの2種類のパーサを用意しそれぞれで、BeautifulSoupオブジェクトを生成する
    soup_pages1 = BeautifulSoup(response.text,'html.parser')
    soup_pages2 = BeautifulSoup(response.text,'lxml')
    count = 0
    for a in selector:
        #両者いずれかのパーサーにてCSSセレクタに該当する要素が一つ以上存在する
        if len(soup_pages1.select(a)) >=1 or len(soup_pages2.select(a)) >=1:
        #html.parserを使用した時に指定したCSSセレクタに一致する要素が、lxmlを使用した時より多いまたは同じ時の処理
            if len(soup_pages1.select(a)) >= len(soup_pages2.select(a)):
                #要素をリストで取得し,1要素ごとに以下の処理を行う
                for i in soup_pages1.select(a):
                    #href属性の値を取得
                    link = i.get('href')
                    #相対urlを絶対urlに変換
                    url2 = urljoin(url,link)
                    #再度クロールを行い次のリンクを辿る。
                    #54行目の※の処理で変数:urlが帰って来たら、その変数:urlをメイン関数に返す。
                    result = crawler(url2,selector)
                    yield from result

        #lxmlを使用したときに指定したCSSセレクタに一致する要素が、html.parserを使用したときより多い時の処理
            elif len(soup_pages2.select(a)) > len(soup_pages1.select(a)):
                for i in soup_pages2.select(a):
                    link = i.get('href')
                    url2 = urljoin(url,link)
                    result = crawler(url2,selector)
                    yield from result
        #CSSセレクターに該当する要素がない場合
        else:
            #上記に該当する場合カウントを1つずつ増やす
            count +=1
            #countが入力したCSSセレクタの数になった時,つまりすべてのCSSセレクタに該当する要素がないとき
            #クロールするページではないと判断させ変数:urlを返す・・・※
            if count ==len(selector):
                global s
                s +=1
                print(s)
                yield url
