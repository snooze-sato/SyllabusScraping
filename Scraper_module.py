from bs4 import BeautifulSoup
import requests
import re
import os
import time

#BeautifulSoup()で第一引数にファイルオブジェクトを指定し、BeautifulSoupオブジェクトを得る
def scraper(url,data):
    syllabus_data ={'university':"",'faculity':"",'department':"",'subject':"",'id':"",'document1':"",'document2':"",'document3':""}

    #response型の取得
    while True:
        try:
            response = requests.get(url)
            break
        except:
            print(
           "********************************\n\
            ********************************\n\
            ********************************\n\
            Pause10000ms\n\
            ********************************\n\
            ********************************\n\
            ********************************\n\
            ")
            time.sleep(10)
    #BeautifulSoupオブジェクトの取得
    soup = BeautifulSoup(response.content,'html.parser')

    #学科学年コードの取得
    #ディレクトリ名を学科学年コードにする
    id1 = os.path.basename(os.path.dirname(url))
    #履修コードの取得
    #ファイル名を履修コードにする
    id2 = os.path.splitext(os.path.basename(url))[0]
    #シラバスデータIDの作成
    id = id1 + id2
    syllabus_data['id'] = id
    print(id)

    #大学名
    university = data['大学名']
    syllabus_data['university']= university

    #bタグで囲まれた箇所の抽出　大学学科　講義名
    for i,b in enumerate(soup.select('b')):
        #学部,学科,講義名を抽出
        if i == 0:
        #学部
            rm = re.compile(r"2.*学\s")
            faculity = rm.sub("", b.text)
            rm = re.compile("(?!.*学部)[^部].*")
            faculity = rm.sub("", faculity)
            syllabus_data['faculity'] = faculity
            print(faculity)
        #学科
            rm = re.compile("2.*学部")
            department = rm.sub("", b.text)
            syllabus_data['department'] = department
            print(department)

    #講義名
    for subject in soup.select(data['講義名抽出セレクタ']):
        subject = subject.text
        syllabus_data['subject'] = subject
        print(subject)


    for koumoku1,document1 in zip(soup.select(data['講義内容1']['項目名抽出セレクタ']),soup.select(data['講義内容1']['内容抽出セレクタ'])):
        if data['講義内容1']['項目名'] in koumoku1.text:
            document1 = document1.text
            print(document1)
            syllabus_data['document1'] =document1

    for koumoku2,document2 in zip(soup.select(data['講義内容2']['項目名抽出セレクタ']),soup.select(data['講義内容2']['内容抽出セレクタ'])):
        if data['講義内容2']['項目名'] in koumoku2.text:
            document2 = document2.text
            print(document2)
            syllabus_data['document2'] =document2

    for koumoku3,document3 in zip(soup.select(data['講義内容3']['項目名抽出セレクタ']),soup.select(data['講義内容3']['内容抽出セレクタ'])):
        if data['講義内容3']['項目名'] in koumoku3.text:
            document3 = document3.text
            print(document3)
            syllabus_data['document3'] =document3

    return syllabus_data
