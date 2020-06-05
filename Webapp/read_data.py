"""
Hanwei Wang
Time: 13-5-2020 11:26
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

import random
from numpy import random as Random
from faker import Faker
from Webapp import db
from Webapp.models import Admin, Category, Post, Deal, User
from sqlalchemy import func
import re
import pandas as pd
import glob

fake = Faker()

def fake_post():
    k = 0
    csv_list = glob.glob(r'Data/*.csv')
    for csv in csv_list:
        try:
            csvDF = pd.read_csv(csv, delimiter=',')
            if csvDF.shape[1] == 1:
                csvDF = pd.read_csv(csv, delimiter=';')
            # print(tempDF)
        except:
            csvDF = pd.read_csv(csv, delimiter=';')
        link_list = csvDF['list'].dropna().tolist()
        avater_list = csvDF['avater'].dropna().tolist()
        truncation = 20
        generic_title_en = csvDF['title_en']
        generic_title_cn = csvDF['title_cn']
        category_en = csvDF['category_en'].dropna()[0]
        category_cn = csvDF['category_cn'].dropna()[0]
        subtitle_en = csvDF['subtitle_en'].dropna()[0]
        subtitle_cn = csvDF['subtitle_cn'].dropna()[0]
        content_en = csvDF['content_en'].dropna()[0]
        content_cn = csvDF['content_cn'].dropna()[0]
        classification = csvDF['classification'].dropna()[0]
        source = csvDF['source'].dropna()[0]
        i = 0
        j = 1
        while i + truncation*2 < len(link_list):
            normal_list = ''
            truncated_list = link_list[i: i + truncation]
            i = i + truncation
            title_en = generic_title_en[0] + ' (' + str(j) + ')'
            title_cn = generic_title_cn[0] + ' (' + str(j) + ')'
            print(title_cn)
            print(len(avater_list))
            avater_raw = random.choice(avater_list)
            avater_list.remove(avater_raw)
            j = j + 1
            p1 = re.compile(r'[(](.*?)[)]', re.S)
            avater = re.findall(p1, avater_raw)[0]
            for url in truncated_list:
                try:
                    p1 = re.compile(r'[(](.*?)[)]', re.S)
                    normal_list = normal_list + (re.findall(p1, url)[0]) + '\\'
                except:
                    pass
        else:
            normal_list = ''
            truncated_list = link_list[i: len(link_list)]
            title_en = generic_title_en[0] + ' (' + str(j) + ')'
            title_cn = generic_title_cn[0] + ' (' + str(j) + ')'
            avater_raw = random.choice(truncated_list)
            p1 = re.compile(r'[(](.*?)[)]', re.S)
            avater = re.findall(p1, avater_raw)[0]
            for url in truncated_list:
                try:
                    p1 = re.compile(r'[(](.*?)[)]', re.S)
                    normal_list = normal_list + (re.findall(p1, url)[0]) + '\\'
                except:
                    pass



if __name__ == '__main__':
    fake_post()








