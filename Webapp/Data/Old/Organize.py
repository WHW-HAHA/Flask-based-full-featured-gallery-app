"""
Hanwei Wang
Time: 22-5-2020 11:01
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

import pandas as pd
import glob
import random
from math import floor

def orgnaize():
    csv_list = glob.glob(r'*.csv')
    for csv in csv_list:
        try:
            csvDF = pd.read_csv(csv, delimiter=',', )
            if csvDF.shape[1] == 1:
                csvDF = pd.read_csv(csv, delimiter=';',)
        except:
            csvDF = pd.read_csv(csv, delimiter=';',)

        link_list = csvDF['list'].dropna().tolist()
        avater_list = csvDF['avater'].dropna().tolist()
        truncation = floor(len(link_list)/len(avater_list))
        generic_title_en = csvDF['title_en'].dropna()
        generic_title_cn = csvDF['title_cn'].dropna()
        category_en = csvDF['category_en'].dropna()[0]
        category_cn = csvDF['category_cn'].dropna()[0]
        subtitle_en = csvDF['subtitle_en'].dropna()[0]
        subtitle_cn = csvDF['subtitle_cn'].dropna()[0]
        content_en = csvDF['content_en'].dropna()[0]
        content_cn = csvDF['content_cn'].dropna()[0]
        source = csvDF['source'].dropna()[0]
        classificaion = csvDF['classification'].dropna()[0]

        i = 0
        j = 1
        avater_len = len(avater_list)
        while i + truncation*2 <= len(link_list):
            truncated_list = link_list[i: i + truncation]
            i = i + truncation
            if avater_len >1:
                title_en = generic_title_en[0] + ' (' + str(j) + ')'
                title_cn = generic_title_cn[0] + ' (' + str(j) + ')'
            else:
                title_en = generic_title_en[0]
                title_cn = generic_title_cn[0]
            avater_raw = random.choice(avater_list)
            avater_list.remove(avater_raw)
            j = j + 1
            new_dataframe = pd.DataFrame({'category_en': category_en,
                                          'category_cn': category_cn,
                                          'subtitle_en': subtitle_en,
                                          'subtitle_cn': subtitle_cn,
                                          'title_en': title_en,
                                          'title_cn': title_cn,
                                          'content_en': content_en,
                                          'content_cn': content_cn,
                                          'source': source,
                                          'classification': classificaion,
                                          'avater': avater_raw,
                                          'list': truncated_list
            })

            new_dataframe.to_csv(title_en+'.csv', sep= ';', encoding='utf_8_sig')
            print(title_en+'done')

        else:
            truncated_list = link_list[i: len(link_list)]
            if avater_len >1:
                title_en = generic_title_en[0] + ' (' + str(j) + ')'
                title_cn = generic_title_cn[0] + ' (' + str(j) + ')'
            else:
                title_en = generic_title_en[0]
                title_cn = generic_title_cn[0]
            avater_raw = random.choice(avater_list)
            new_dataframe = pd.DataFrame({'category_en': category_en,
                                          'category_cn': category_cn,
                                          'subtitle_en': subtitle_en,
                                          'subtitle_cn': subtitle_cn,
                                          'title_en': title_en,
                                          'title_cn': title_cn,
                                          'content_en': content_en,
                                          'content_cn': content_cn,
                                          'source': source,
                                          'classification': classificaion,
                                          'avater': avater_raw,
                                          'list': truncated_list
            })
            new_dataframe.to_csv(title_en+'.csv', sep= ';',encoding='utf_8_sig')
            print(title_en+'done')

if __name__ == '__main__':
    orgnaize()