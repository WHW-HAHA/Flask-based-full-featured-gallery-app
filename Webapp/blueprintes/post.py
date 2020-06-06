"""
Hanwei Wang
Time: 13-2-2020 10:19
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from flask import Blueprint, render_template, request
from flask_login import current_user
from Webapp.models import Post, User
from Webapp.extensions import db
from sqlalchemy import or_

post_bp = Blueprint('post', __name__)

@post_bp.route("/en/<post_id>") # post_id 在这个route函数被调用时传入
def post_en(post_id):
    post = Post.query.get_or_404(post_id)
    picture_list = post.picture_list
    picture_list = picture_list.split('+')
    print(picture_list)
    name = post.title_en.split('(')[0]
    # get posts with similar category, and show 5 of them
    # category = post.categories
    # category = Category.query.get(post.categories)
    post_found = Post.query.filter(or_(
        Post.title_en.like('%' + name + '%') if name is not None else [],
        Post.subtitle_en.like('%' + name + '%') if name is not None else [],
        Post.content_en.like('%' + name + '%') if name is not None else [],
    ))
    like_posts = post_found.order_by(Post.date_posted.desc()).all()
    if post.classification =='vip1':
        if current_user.is_authenticated:
            if current_user.vip1 == 'yes':
                return render_template('en_post_content.html', title=post.title_en, post=post, picture_list=picture_list[:-1],
                                       like_posts=like_posts)
            else:
                return render_template('404_not_allowed_to_visit.html')
        else:
            return render_template('404_not_allowed_to_visit.html')

    elif post.classification == 'vip2':
        if current_user.is_authenticated:
            if current_user.vip2 == 'yes':
                return render_template('en_post_content.html', title=post.title_en, post=post, picture_list=picture_list[:-1],
                                       like_posts=like_posts)
            else:
                return render_template('404_not_allowed_to_visit.html')
        else:
            return render_template('404_not_allowed_to_visit.html')

    else:
        return render_template('en_post_content.html', title=post.title_en, post=post, picture_list = picture_list[:-1], like_posts = like_posts[0:8])

@post_bp.route("/cn/<post_id>") # post_id 在这个route函数被调用时传入
def post_cn(post_id):
    post = Post.query.get_or_404(post_id)
    picture_list = post.picture_list
    picture_list = picture_list.split('+')
    name = post.title_cn.split('(')[0]
    # get posts with similar category, and show 5 of them
    # category = post.categories
    # category = Category.query.get(post.categories)
    post_found = Post.query.filter(or_(
        Post.title_cn.like('%' + name + '%') if name is not None else [],
        Post.subtitle_cn.like('%' + name + '%') if name is not None else [],
        Post.content_cn.like('%' + name + '%') if name is not None else [],
    ))
    like_posts = post_found.order_by(Post.date_posted.desc()).all()
    if post.classification =='vip1':
        if current_user.is_authenticated:
            if current_user.vip1 == 'yes':
                return render_template('cn_post_content.html', title=post.title_cn, post=post, picture_list=picture_list[:-1],
                                       like_posts=like_posts)
            else:
                return render_template('404_not_allowed_to_visit.html')
        else:
            return render_template('404_not_allowed_to_visit.html')

    elif post.classification == 'vip2':
        if current_user.is_authenticated:
            if current_user.vip2 == 'yes':
                return render_template('cn_post_content.html', title=post.title_cn, post=post, picture_list=picture_list[:-1],
                                       like_posts=like_posts)
            else:
                return render_template('404_not_allowed_to_visit.html')
        else:
            return render_template('404_not_allowed_to_visit.html')

    else:
        return render_template('cn_post_content.html', title=post.title_cn, post=post, picture_list = picture_list[:-1], like_posts = like_posts[0:8])


@post_bp.route('/en/<post_id>/add_favourite', methods = ['POST'])
def add_favourite_post_page_en(post_id):
    post_id = request.get_json()['post_id']
    post = Post.query.filter_by(id = post_id).first()

    if current_user.is_authenticated:
        if post in current_user.like:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.remove(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            return render_template('en_post_content_section_welcome.html', post=post, header='Succeed',
                                   message='has been removed from your favourite list!')

        else:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.append(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            return render_template('en_post_content_section_welcome.html', post=post, header='Succeed',
                                   message='has been added in your favourite list!')

    else:
        return render_template('en_post_content_section_welcome.html', post = post,header = 'Failed', message = "You haven't log in yet, please please login or register!")


@post_bp.route('/cn/<post_id>/add_favourite', methods = ['POST'])
def add_favourite_post_page_cn(post_id):
    post_id = request.get_json()['post_id']
    post = Post.query.filter_by(id = post_id).first()

    if current_user.is_authenticated:
        if post in current_user.like:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.remove(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            return render_template('cn_post_content_section_welcome.html', post=post, header='成功',
                                   message='已经从您的收藏列表中移除！')

        else:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.append(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            return render_template('cn_post_content_section_welcome.html', post=post, header='成功',
                                   message='已经添加到您的收藏列表！')

    else:
        return render_template('cn_post_content_section_welcome.html', post=post, header='失败', title_hidden=1,
                                   message="您还没有登录，请先登录或注册!")

