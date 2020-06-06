"""
Hanwei Wang
Time: 16-2-2020 18:31
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
"""

'''
fake 数据只能从父类插入
'''
import random
from numpy import random as Random
from faker import Faker
from Webapp import db
from Webapp.models import Admin, Category, Post, Deal, User
from sqlalchemy import func
import re
import pandas as pd
import glob
from math import floor
from datetime import datetime, timedelta



# 建立1侧的模型，虚拟数据可以之后从多侧生成

fake = Faker()

def fake_category():
    categeory_list= ["Category1", "Category2", "Category3", 'Category4']
    for name in categeory_list:
        category = Category( name = name,)
        db.session.add(category)
    db.session.commit()

def update_post():
    categories = Category.query.all()
    csv_list = glob.glob(r'Webapp/Data/to_deploy/*.csv')
    k = 0
    for csv in csv_list:
        try:
            csvDF = pd.read_csv(csv, delimiter=',', encoding='utf_8_sig')
            if csvDF.shape[1] == 1:
                csvDF = pd.read_csv(csv, delimiter=';', encoding='utf_8_sig')
        except:
            csvDF = pd.read_csv(csv, delimiter=';', encoding='utf_8_sig')
        link_list = csvDF['list'].dropna().tolist()
        avater_list = csvDF['avater'].dropna().tolist()
        truncation = floor(len(link_list)/len(avater_list))
        generic_title_en = csvDF['title_en']
        generic_title_cn = csvDF['title_cn']
        category_en = csvDF['category_en'].dropna()[0]
        if category_en == 'asia':
            category_en = categories[0]
        elif category_en == 'USA' or category_en == 'usa':
            category_en = categories[1]
        elif category_en == 'cartoon':
            category_en = categories[2]
        subtitle_en = csvDF['subtitle_en'].dropna()[0]
        subtitle_cn = csvDF['subtitle_cn'].dropna()[0]
        content_en = csvDF['content_en'].dropna()[0]
        content_cn = csvDF['content_cn'].dropna()[0]
        classification = csvDF['classification'].dropna()[0]
        source = csvDF['source'].dropna()[0]
        normal_list = ''
        truncated_list = link_list
        title_en = generic_title_en[0]
        title_cn = generic_title_cn[0]
        avater_raw = avater_list[0]
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        avater = re.findall(p1, avater_raw)[0]
        for url in truncated_list:
            try:
                p1 = re.compile(r'[(](.*?)[)]', re.S)
                normal_list = normal_list + (re.findall(p1, url)[0]) + '\\'
            except:
                pass
        post = Post(title_en = 'Title',
                    title_cn = '标题',
                    subtitle_en = 'Subtitle',
                    subtitle_cn = '副标题',
                    content_cn = '内容',
                    content_en = 'Content',
                    date_posted= datetime.utcnow()+timedelta(hours = random.randint(1,10)),
                    avater='https://user-images.githubusercontent.com/43483189/83882475-76bd0280-a742-11ea-9329-6c196c1f58bf.png',
                    picture_list=['https://user-images.githubusercontent.com/43483189/83882595-a409b080-a742-11ea-9e4e-2d0a84258029.png']*30,
                    classification=classification,
                    source=source,
                    )
        post.categories.append(category_en)
        db.session.add(post)
    db.session.commit()

def fake_post():
    categories = Category.query.all()
    csv_list = glob.glob(r'Webapp/Data/deployed/*.csv')
    k = 0
    for csv in csv_list:
        # print(csv)
        # try:
        #     csvDF = pd.read_csv(csv, delimiter=',', encoding='utf_8_sig')
        #     if csvDF.shape[1] == 1:
        #         csvDF = pd.read_csv(csv, delimiter=';', encoding='utf_8_sig')
        # except:
        csvDF = pd.read_csv(csv, delimiter=';', encoding='utf_8_sig')
        print(csvDF)
        link_list = csvDF['list'].dropna().tolist()
        avater_list = csvDF['avater'].dropna().tolist()
        truncation = floor(len(link_list)/len(avater_list))
        generic_title_en = csvDF['title_en']
        generic_title_cn = csvDF['title_cn']
        category_en = csvDF['category_en'].dropna()[0]
        if category_en == 'asia':
            category_en = categories[0]
        elif category_en == 'USA' or category_en == 'usa':
            category_en = categories[1]
        elif category_en == 'cartoon':
            category_en = categories[2]
        subtitle_en = csvDF['subtitle_en'].dropna()[0]
        subtitle_cn = csvDF['subtitle_cn'].dropna()[0]
        content_en = csvDF['content_en'].dropna()[0]
        content_cn = csvDF['content_cn'].dropna()[0]
        classification = csvDF['classification'].dropna()[0]
        source = csvDF['source'].dropna()[0]
        normal_list = ''
        truncated_list = link_list
        title_en = generic_title_en[0]
        title_cn = generic_title_cn[0]
        avater_raw = avater_list[0]
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        avater = re.findall(p1, avater_raw)[0]
        for url in truncated_list:
            try:
                p1 = re.compile(r'[(](.*?)[)]', re.S)
                normal_list = normal_list + (re.findall(p1, url)[0]) + '\\'
            except:
                pass
        post = Post(title_en = 'Title',
                    title_cn = '标题',
                    subtitle_en = 'Subtitle',
                    subtitle_cn = '副标题',
                    content_cn = '内容',
                    content_en = 'Content',
                    date_posted= datetime.utcnow()+timedelta(hours = random.randint(1,10)),
                    avater='https://user-images.githubusercontent.com/43483189/83882475-76bd0280-a742-11ea-9329-6c196c1f58bf.png',
                    picture_list='https://user-images.githubusercontent.com/43483189/83882595-a409b080-a742-11ea-9e4e-2d0a84258029.png+'*30,
                    classification=classification,
                    source=source,
                    )
        post.categories.append(category_en)
        db.session.add(post)
    db.session.commit()

def fake_admin():
    admin = Admin(
            superusername = 'Hanwei_1',
    )
    admin.set_password('Whw844409040')
    db.session.add(admin)
    admin = Admin(
            superusername = 'Hanwei_2',
    )
    admin.set_password('Whw844409040')
    db.session.add(admin)
    db.session.commit()

def fake_user(count = 50):
    for i in range(count):
        membership = random.choice(['none', 'week', 'month', 'year'])
        if membership == 'none':
            vip1 = 'no'
            vip2 = 'no'
        else:
            vip1 = 'yes'
            vip2 = random.choice(['yes', 'no'])

        user = User(username = fake.name(),
                    email = fake.email(),
                    password = 'Whw8409040',
                    membership = membership,
                    vip1 = vip1,
                    vip2 = vip2,
                    invitation_code_vip1 = generate_verification_code(),
                    invitation_code_vip2 = generate_verification_code()
                    )

        for j in range(random.randint(1, 5)):
            post = Post.query.get(random.randint(1, Post.query.count()))
            if post not in user.like:
                user.like.append(post)
    db.session.commit()

def generate_verification_code():
    code_list = []
    for i in range(10): # 0-9数字
        code_list.append(str(i))
    # for i in range(65, 91): # A-Z
    #     code_list.append(chr(i))
    # for i in range(97, 123): # a-z
    #     code_list.append(chr(i))

    myslice = random.sample(code_list, 8)  # 从list中随机获取12个元素，作为一个片断返回
    share_code = ''.join(myslice) # list to string
    return share_code

def fake_deal(count = 100):
    for i in range(count):
        deal = Deal(time = fake.date_of_birth(),
                    by = User.query.get(random.randint(1, User.query.count())),
                    what = Post.query.get(random.randint(1, Post.query.count()))
                    )
        db.session.add(deal)
    db.session.commit()

# def fake_category():
#     categeory_list = ["The latest", "Asia", "Europe & USA", "Cartoon", 'Unclassified']
#     for Name in categeory_list:
#         category = Category( name = Name,
#                               description = fake.sentence(),
#                               # admin = Admin.query.get(random.randint(1, 2))
#                               )
#         posts = Post.query.all()
#
#         for j in Random.randint(50, size=10):
#             post = posts[j]
#             category.posts.append(post)
#         db.session.add(category)
#     db.session.commit()

def fake_count():

    for post in Post.query.all():
        post.total_like = len(post.likeby)
        post.total_buy = len(post.deals)
    db.session.commit()











