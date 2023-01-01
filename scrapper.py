#!/usr/bin/env python
# coding: utf-8


import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import time as t


# According to the given url, Parse_Mobile01 will return the parse dataframe,
# which include the information of the article's tilte, link and category .
def Parse_Mobile01(uri):
    # uri = "https://www.mobile01.com/forumtopic.php?c=23"
    req = urllib.request.Request(
        uri,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    handle = urllib.request.urlopen(req)
    encoding = handle.headers.get_content_charset()
    html_data = handle.read().decode(encoding)

    soup = BeautifulSoup(html_data, 'html.parser')
    # title = soup.find_all("a", class_="c-link u-ellipsis")
    title = soup.select('div.c-listTableTd__title a.c-link.u-ellipsis')
    creator = soup.select('div.l-listTable__td.l-listTable__td--time div a.c-link.u-ellipsis.u-username')
    timestamp = soup.select('div.l-listTable__td.l-listTable__td--time div.o-fNotes')
    feedback = soup.select('div.l-listTable__td.l-listTable__td--count div.o-fMini')

    title_text_list = []
    title_href_list = []
    title_category_list = []
    title_id_list = []
    creator_name_list = []
    creat_timestamp_list = []
    feedback_count_list = []

    # print(title)
    # print(creator)
    # print(timestamp)
    # print(feedback)

    # Parsing title data
    for i in title:
        try:
            title_text = i.text
            title_href = "https://www.mobile01.com/" + i.get("href")
            title_category = re.findall(r"f=(\d+)", i.get("href"))[0]
            title_id = re.findall(r"t=(\d+)", i.get("href"))[0]

            title_text_list.append(title_text)
            title_href_list.append(title_href)
            title_category_list.append(title_category)
            title_id_list.append(int(title_id))
        except:
            title_text_list.append('')
            title_href_list.append('')
            title_category_list.append('')
            title_id_list.append('')

        print(title_text)
        print(title_href)
        print(title_category)
        print(title_id)
        print("-----------------------------------------------")

    # Parsing creator data
    count = 0
    for i in creator:
        if count%2 == 0:
            try:
                creator_name = i.text
                creator_name_list.append(creator_name)
            except:
                creator_name_list.append('')
        else:
            pass
        count += 1


    # Parsing creat_timestamp data
    count = 0
    for i in timestamp:
        if count%2 == 0:
            try:
                creat_timestamp = i.text
                creat_timestamp_list.append(creat_timestamp)
            except:
                creat_timestamp_list.append('')
        else:
            pass
        count += 1



    # Parsing feedback data
    for i in feedback:
        try:
            feedback_count = int(i.text)
            feedback_count_list.append(feedback_count)
        except:
            feedback_count_list.append(0)



    result_df = pd.DataFrame(
        list(zip(title_id_list, title_text_list, title_href_list, title_category_list, creator_name_list,creat_timestamp_list,feedback_count_list)),
        columns=['article_id', 'title', 'link', 'category', 'creator', 'creat_timestamp','feedback'])
    result_df['creat_timestamp'] = pd.to_datetime(result_df['creat_timestamp'], format='%Y-%m-%d %H:%M')
    return (result_df)


# Main
if __name__ == "__main__":
    # Scrapping mobile01 page by page
    for i in range(1, 21):
        print("=================== PAGE {} ===================".format(i))

        url_str = "https://www.mobile01.com/forumtopic.php?c=23&p=" + str(i)
        temp_df = Parse_Mobile01(url_str)

        if i == 1:
            mobile01_df = temp_df
        else:
            mobile01_df = mobile01_df.append(temp_df, ignore_index=True)
        t.sleep(3)

    print(mobile01_df)

    # Input data into DB
    # TODO: change to update > https://stackoverflow.com/questions/31988322/pandas-update-sql
    try:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost:3306/{db}"
                               .format(user="test_user",
                                       pw="HollyHsiao89!",
                                       db="test"))

        mobile01_df.set_index('article_id', inplace=True)
        mobile01_df.to_sql('mobile01', con=engine, if_exists='replace', chunksize=100000)
        print("Successfully insert into DB !")

    except Exception as e:
        print("Error! >>" + (e))

# TODO: Airflow> Daily