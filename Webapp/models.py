"""
Hanwei Wang
Time: 13-2-2020 10:20
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from datetime import datetime
from Webapp.extensions import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
# werkzeug 路由模块
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

'''
instance

class Author(db.Model):
    __tablename__ = 'info_author'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    # 一的一方，relationship为Author 添加article属性，Author_obj.article内容是以Author_obj.id == Article.author_id的一组Article对象
    # back_populates（反向引用） 则为Article添加author属性，Article_obj.author内容是以Article.author_id == Author_obj.id 的Author_obj
    article = db.relationship("Article",back_populates='author',lazy='dynamic')
    

#2 关系表， db.relationship() 在多侧和一侧都可以建立但是同时建立时， 
    
    back_populates意味着可以从多端访问一端，
    class Father(..): 
    children = relationship( 'Child', back_populates='parent' )
    
    然而从一端定义的关系表是正向访问，不需要back_populates
    class Father(..): 
        id = Column(..)
        children = relationship('Child')

    class Child(..):
        father_id = Column( Integer, ForeignKey('father.id') )
    
    
#3 lazy: 指定sqlalchemy数据库什么时候加载数据
        select: 就是访问到属性的时候，就会全部加载该属性的数据
        joined: 对关联的两个表使用联接
        subquery: 与joined类似，但使用子子查询
        dynamic: 不加载记录，但提供加载记录的查询，也就是生成query对象
    
    class Article(db.Model):
        __tablename__ = "info_article"
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(20),nullable=False)
        # 多的一方，author_id 的取值范围只能在info_author.id的范围内
        author_id = db.Column(db.Integer,db.ForeignKey('info_author.id'))
'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Administrator class
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    superusername = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    # relationships

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(db.Model, UserMixin):
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=False, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String, nullable=False, default='default profile.jpg')
    membership = db.Column(db.String, nullable = False, default='none') # False or True
    membership_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    vip1 = db.Column(db.String, nullable = False, default='none')
    vip1_try_out = db.Column(db.String, nullable = False, default = 'yes')
    vip1_expire_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    vip2 = db.Column(db.String, nullable = False, default='none')
    vip2_try_out = db.Column(db.String, nullable = False, default = 'yes')
    vip2_expire_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    invitation_code_vip1 = db.Column(db.String(8), nullable = True)
    invitation_code_vip2 = db.Column(db.String(8), nullable = True)
    deals = db.relationship('Deal', backref = 'by')

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id} ).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Deal(db.Model):
    # 1 user to multi deals
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('post.id'))

# post 和 category 实际为多对多，应该创建关联表进行连接
post_category_collections = db.Table("post_category_collections",
                                     db.Column('post_id', db.Integer, db.ForeignKey("post.id")),
                                     db.Column('category_id', db.Integer, db.ForeignKey("category.id")))

# one user can like many posts and a post can be followed by many users
# 关联表意味着每一行 都是一个表的id 对应另一个标的 id post_id --> user_id
post_user_colloections = db.Table('post_user_collections',
                                  db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')))
class Post(db.Model):
    __tablename__ = 'post'
    __searchable__  =  ['title_en', 'title_cn', 'subtitle_en', 'subtitle_cn', 'content_en', 'content_cn']
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(20), nullable=False)
    title_cn = db.Column(db.String(20), nullable=False)
    subtitle_en = db.Column(db.String(100), nullable = False)
    subtitle_cn = db.Column(db.String(100), nullable = False)
    content_en = db.Column(db.Text, nullable=False)
    content_cn = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Integer, nullable = False, default = 0)
    image_file = db.Column(db.String, nullable = False, default = 'LiyuanLing.png')
    source = db.Column(db.String, nullable = True, default= 'ins')
    avater = db.Column(db.String, nullable = True)
    picture_list =db.Column(db.String, nullable = True)
    classification = db.Column(db.String, nullable = False, default = 'vip2')
    #relationships
    deals = db.relationship('Deal', backref = 'what')
    # category_id = db.relationship("Category", secondary= post_category_collections, backref = "posts", lazy = 'dynamic')
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = True, default = 'unclassified')
    categories = db.relationship('Category', secondary = post_category_collections, backref= 'posts')
    likeby = db.relationship('User', secondary =post_user_colloections, backref = 'like')
    total_like = db.Column(db.Integer, nullable = True, default = 0)
    total_buy = db.Column(db.Integer, nullable = True, default = 0)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)
    description = db.Column(db.String(100), nullable = True)
    image_file = db.Column(db.String, nullable = False, default = 'default category.jpg')

