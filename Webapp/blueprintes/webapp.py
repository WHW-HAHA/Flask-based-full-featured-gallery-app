"""
Hanwei Wang
Time: 26-2-2020 15:49
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""

from flask import send_from_directory, Blueprint, render_template, redirect, url_for, flash,request
from Webapp.models import Post, User, Category
from sqlalchemy import or_
from flask_login import current_user
from Webapp.extensions import db
from datetime import datetime, timedelta
import json
webapp_bp = Blueprint('webapp', __name__)

# default language is English

global lang
lang = 'en'

# static file
@webapp_bp.route('/sitemap.xml')
def static_from_root():
    return send_from_directory('static', request.path[1:])

@webapp_bp.route('/ByteDanceVerify.html')
def ByteDanceVerify_root():
    return send_from_directory('static', request.path[1:])

@webapp_bp.route('/language', methods=['POST'])
def get_defaulte_language():
    default_laguage = request.get_json()
    if default_laguage is not None:
        print('language is')
        print(default_laguage)
        global lang
        lang = default_laguage['lang']
        with open('language.json', 'w') as f:
            json.dump({'lang': lang}, f)
            f.close()
    return 'language'

@webapp_bp.route('/')
@webapp_bp.route('/welcome')
def welcome():
    category2 = Category.query.get(1)
    category3 = Category.query.get(2)
    category4 = Category.query.get(3)
    post_list_1 = Post.query.order_by(Post.date_posted.desc()).all()[0:5]
    post_list_2 = category2.posts[0:5]
    post_list_3 = category3.posts[0:5]
    post_list_4 = category4.posts[0:5]
    post_list_5 = (Post.query.filter(or_(Post.classification=='vip1',
                                  Post.classification == 'vip2')).all())

    if lang == 'en':
        return render_template('en_welcome.html', title = 'Welcome', lang = 'en', category_asia=category2, category_usa=category3, category_cartoon=category4,
                           list1=post_list_1, list2=post_list_2, list3=post_list_3, list4=post_list_4, list5=post_list_5)
    else:
        return render_template('cn_welcome.html', title = '欢迎', lang ='cn', category_asia=category2, category_usa=category3, category_cartoon=category4,
                           list1=post_list_1, list2=post_list_2, list3=post_list_3, list4=post_list_4, list5=post_list_5)

@webapp_bp.route('/gotocategory/<name>')
def go_to_category(name):
    if name == 'TheLatest':
        category_name = 'The Latset'
        category = Category.query.filter_by(name=category_name).first()
        posts = Post.query.all()[0:12]
        if lang == 'en':
            return render_template('en_category_content.html', title = 'Category 1', category=category, posts=posts)
        else:
            return render_template('cn_category_content.html', title = '分类一', category=category , posts=posts)
    else:
        category_name = name
        category = Category.query.filter_by(name=category_name).first()
        posts = category.posts
        if category_name == 'asia':
            if lang == 'en':
                return render_template('en_category_content.html', title='Category 3', category=category, posts=posts)
            else:
                category.name = '亚洲'
                return render_template('cn_category_content.html', title ='分类三', category=category, posts=posts)
        else:
            if lang == 'en':
                return render_template('en_category_content.html', title='Category 4', category=category, posts=posts)
            else:
                category.name = '卡通'
                return render_template('cn_category_content.html', title='分类四', category=category, posts=posts)

def take_total_like(elem):
    return elem.total_like


def take_time_posted(elem):
    return elem.date_posted


def bubbleSort_by_totallike(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j].total_like < nums[j + 1].total_like:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


def bubbleSort_by_time(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j].date_posted < nums[j + 1].date_posted:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


@webapp_bp.route('/gotocategory/<categoryName>/sorted', methods=['POST'])
def sort_content_TheLatest(categoryName):
    sort_by = request.get_json()['by']
    category = Category.query.filter_by(name=categoryName).first()
    if sort_by == 'popularity':
        posts_all = Category.query.filter_by(name=categoryName).first().posts
        posts = bubbleSort_by_totallike(list(posts_all))
    if sort_by == 'time':
        posts_all = Category.query.filter_by(name=categoryName).first().posts
        posts = bubbleSort_by_time(list(posts_all))
    if lang == 'en':
        return render_template('en_category_content_section.html', title = categoryName, posts=posts, category=category)
    else:
        return render_template('cn_category_content_section.html', title = categoryName, posts=posts, category= category)


@webapp_bp.route('/search/sorted', methods=['POST'])
def sort_content_search():
    sort_by = request.get_json()['by']
    keyword = request.get_json()['keyword']
    if lang == 'en':
        post_found = Post.query.filter(or_(
            Post.title_en.like('%' + keyword + '%') if keyword is not None else '',
            Post.subtitle_en.like('%' + keyword + '%') if keyword is not None else '',
            Post.content_en.like('%' + keyword + '%') if keyword is not None else '',))
    else:
        post_found = Post.query.filter(or_(
            Post.title_cn.like('%' + keyword + '%') if keyword is not None else '',
            Post.subtitle_cn.like('%' + keyword + '%') if keyword is not None else '',
            Post.content_cn.like('%' + keyword + '%') if keyword is not None else ''))
    posts = post_found.all()
    title = "Results of {}".format(keyword)

    if sort_by == 'popularity':
        posts = bubbleSort_by_totallike(list(posts))
    if sort_by == 'time':
        posts = bubbleSort_by_time(list(posts))
    if lang == 'en':
        return render_template('en_search_content_section.html', title= title,lang = lang, posts=posts)
    else:
        return render_template('cn_search_content_section.html', title= title,lang = lang, posts=posts)


@webapp_bp.route('/add_favourite', methods=['POST'])
def add_favourite_welcome_page():
    post_id = request.get_json()['post_id']
    lang= request.get_json()['lang']
    post = Post.query.filter_by(id = post_id).first()
    if current_user.is_authenticated:
        if post in current_user.like:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.remove(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            if lang == 'en':
                return render_template('en_post_content_section_welcome.html', post=post, header='Succeed',
                                   message='has been removed from your favourite list!')
            else:
                return render_template('cn_post_content_section_welcome.html', post=post, header='成功',
                                       message='已经从您的收藏列表中移除!')
        else:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.append(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            if lang == 'en':
                return render_template('en_post_content_section_welcome.html', post=post, header='Succeed',
                                   message='has been added in your favourite list!')
            else:
                return render_template('cn_post_content_section_welcome.html', post=post, header='成功',
                                       message='已经添加到您的收藏列表!')
    else:
        if lang == 'en':
            return render_template('en_post_content_section_welcome.html',header='Failed', post = post, title_hidden = 1,
                               message="You haven't log in yet, please please login or register!")
        else:
            return render_template('cn_post_content_section_welcome.html',header='失败', post = post, title_hidden = 1,
                                   message="您还没有登录，请先登录或注册！")


@webapp_bp.route('/gotocategory/<categoryName>/add_favourite', methods=['POST'])
def add_favourite_content_page(categoryName):
    categoryName = request.get_json()['categoryName']
    post_id = request.get_json()['post_id']
    lang= request.get_json()['lang']
    post = Post.query.filter_by(id = post_id).first()

    category = Category.query.filter_by(name=categoryName).first()
    print(post)
    if current_user.is_authenticated:
        if post in current_user.like:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.remove(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            if lang == 'en':
                return render_template('en_post_content_section_category.html', post=post, header='Succeed',category=category,
                                   message='has been removed from your favourite list!')
            else:
                return render_template('cn_post_content_section_category.html', post=post, header='成功', category=category,
                                       message='已经从您的收藏列表中移除！')
        else:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.append(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            if lang == 'en':
                return render_template('en_post_content_section_category.html', post=post, header='Succeed',category=category,
                                   message='has been added in your favourite list!')
            else:
                return render_template('cn_post_content_section_category.html', post=post, header='成功',category=category,
                                   message='已经添加到您的收藏列表!')
    else:
        if lang == 'en':
            return render_template('en_post_content_section_category.html',header='Failed', category=category, title_hidden = 1,post= post,
                               message="You haven't log in yet, please please login or register!")
        else:
            return render_template('cn_post_content_section_category.html', header='失败', title_hidden = 1, post = post,
                                   category=category, message="您还没有登录，请先登录或注册!")


@webapp_bp.route('/search/add_favourite', methods=['POST'])
def add_favourite_search_page():
    post_id = request.get_json()['post_id']
    lang= request.get_json()['lang']
    post = Post.query.filter_by(id = post_id).first()

    if current_user.is_authenticated:
        if post in current_user.like:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.remove(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            if lang == 'en':
                return render_template('en_search_post_content_section.html', post=post, header='Succeed',
                                   message='has been removed from your favourite list!')
            else:
                return render_template('cn_search_post_content_section.html', post=post, header='成功',
                                   message='已经从您的收藏列表中移除！')
        else:
            user = User.query.filter_by(id=current_user.id).first()
            user.like.append(post)
            db.session.commit()
            post.total_like = len(post.likeby)
            db.session.commit()
            if lang == 'en':
                return render_template('en_search_post_content_section.html', post=post, header='Succeed',
                                   message='has been added in your favourite list!')
            else:
                return render_template('cn_search_post_content_section.html', post=post, header='成功',
                                   message='已经添加到您的收藏列表！')
    else:
        if lang == 'en':
            return render_template('en_post_content_section_welcome.html', post=post, header='Failed', title_hidden = 1,
                               message="You haven't log in yet, please please login or register!")
        else:
            return render_template('cn_post_content_section_welcome.html', post=post, header='失败', title_hidden = 1,
                               message="您还没有登录，请先登录或注册!")


@webapp_bp.route("/home")
def home():
    category_id = 0
    # this page should gives all the posts in different page
    page = request.args.get('page', 1, type=int)
    # get the page number of current page
    # if category is a valid category name
    if category_id == 0:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    else:
        posts = Category.query.get(category_id).posts.order_by(Post.date_posted.desc()).paginate(page, per_page=5)
    for post in Post.query.all():
        post.total_likes = len(list(post.likeby))
    categories = Category.query.all()
    return render_template('home.html', posts=posts, categories=categories)


@webapp_bp.route("/category")
def show_category():
    page = request.args.get('page', 1, type=int)
    posts = Category.query.filter_by(name='The latest').first().posts
    if lang == 'en':
        return render_template('en_category_content.html', posts=posts, category_name='The latest')
    else:
        return render_template('cn_category_content.html', posts=posts, category_name='The latest')


@webapp_bp.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        # get keyword variable from form in web page
        ## search in user is no need
        keyword = request.form.get('keyword')
        if keyword == "":
            return render_template('search_nofound.html', title='No Result', keyword=keyword)
        else:
            if lang == 'en':
                post_found = Post.query.filter(or_(
                    Post.title_en.like('%' + keyword + '%') if keyword is not None else '',
                    Post.subtitle_en.like('%' + keyword + '%') if keyword is not None else '',
                    Post.content_en.like('%' + keyword + '%') if keyword is not None else '',
                    Post.title_cn.like('%' + keyword + '%') if keyword is not None else '',
                    Post.subtitle_cn.like('%' + keyword + '%') if keyword is not None else '',
                    Post.content_cn.like('%' + keyword + '%') if keyword is not None else '',
                ))
            else:
                post_found = Post.query.filter(or_(
                    Post.title_cn.like('%' + keyword + '%') if keyword is not None else '',
                    Post.subtitle_cn.like('%' + keyword + '%') if keyword is not None else '',
                    Post.content_cn.like('%' + keyword + '%') if keyword is not None else '',
                    Post.title_en.like('%' + keyword + '%') if keyword is not None else '',
                    Post.subtitle_en.like('%' + keyword + '%') if keyword is not None else '',
                    Post.content_en.like('%' + keyword + '%') if keyword is not None else '',
                ))

            post = post_found.order_by(Post.date_posted.desc()).all()
            title_en = 'Results of {}'.format(keyword)
            title_cn = '关于{}的内容'.format(keyword)
            # highlight the keyword in result page
            if lang == 'en':
                if post_found.all():
                    flash('We had found these for you!', 'success')
                    return render_template('en_search_found.html', lang = lang, title= title_en, posts=post, keyword=keyword)
                else:
                    return render_template('search_nofound.html',lang = lang, title='No result', keyword=keyword)
            else:
                if post_found.all():
                    flash('我们为您找到了这些内容！', 'success')
                    return render_template('cn_search_found.html', lang = lang, title= title_cn, posts=post, keyword=keyword)
                else:
                    return render_template('search_nofound.html', lang = lang, title='No result', keyword=keyword)


@webapp_bp.route("/en/get_temporary_vip1")
def three_days_VIP1_en():
    if current_user.vip1_try_out == 'yes':
        current_user.vip1_expire_date = datetime.now()
        expire_date = current_user.vip1_expire_date + timedelta(days=5)
        user = User.query.filter_by(id=current_user.id).first()
        user.vip1_try_out = 'no'
        user.vip1_expire_date = expire_date
        user.vip1 = 'yes'
        db.session.commit()
        flash("Enjoy your exploration, your temporary VIP1 will expire in 5 days.", 'success')
        return redirect(url_for('webapp.welcome'))
    else:
        invitation_code_vip1 = current_user.invitation_code_vip1
        invitation_code_vip2 = current_user.invitation_code_vip2
        return render_template('invitation_code.html', title = 'Get free VIP1', code1=invitation_code_vip1, code2=invitation_code_vip2)


@webapp_bp.route("/cn/get_temporary_vip1")
def three_days_VIP1_cn():
    if current_user.vip1_try_out == 'yes':
        current_user.vip1_expire_date = datetime.now()
        expire_date = current_user.vip1_expire_date + timedelta(days=5)
        user = User.query.filter_by(id=current_user.id).first()
        user.vip1_try_out = 'no'
        user.vip1_expire_date = expire_date
        user.vip1 = 'yes'
        db.session.commit()
        flash("您的临时VIP1将在5天内到期, 在此之前请尽情体验我们的内容。", 'success')
        return redirect(url_for('webapp.welcome'))
    else:
        invitation_code_vip1 = current_user.invitation_code_vip1
        invitation_code_vip2 = current_user.invitation_code_vip2
        return render_template('invitation_code.html', title = '获得免费VIP', code1=invitation_code_vip1, code2=invitation_code_vip2)

@webapp_bp.route("/en/get_temporary_vip2")
def one_day_VIP2_en():
    if current_user.vip2_try_out == 'yes':
        current_user.vip2_expire_date = datetime.now()
        expire_date = current_user.vip2_expire_date + timedelta(days=3)
        user = User.query.filter_by(id=current_user.id).first()
        user.vip2_try_out = 'no'
        user.vip2_expire_date = expire_date
        user.vip2 = 'yes'
        db.session.commit()
        flash("Enjoy your exploration, your temporary VIP2 will expire in 3 days.", 'success')
        return redirect(url_for('webapp.welcome'))
    else:
        invitation_code_vip1 = current_user.invitation_code_vip1
        invitation_code_vip2 = current_user.invitation_code_vip2
        return render_template('invitation_code.html', title= 'Get free VIP',code1=invitation_code_vip1, code2=invitation_code_vip2)

@webapp_bp.route("/cn/get_temporary_vip2")
def one_day_VIP2_cn():
    if current_user.vip2_try_out == 'yes':
        current_user.vip2_expire_date = datetime.now()
        expire_date = current_user.vip2_expire_date + timedelta(days=3)
        user = User.query.filter_by(id=current_user.id).first()
        user.vip2_try_out = 'no'
        user.vip2_expire_date = expire_date
        user.vip2 = 'yes'
        db.session.commit()
        flash("您的临时VIP2将在3天内到期, 在此之前请尽情体验我们的内容。", 'success')
        return redirect(url_for('webapp.welcome'))
    else:
        invitation_code_vip1 = current_user.invitation_code_vip1
        invitation_code_vip2 = current_user.invitation_code_vip2
        return render_template('invitation_code.html',title='获得免费VIP', code1=invitation_code_vip1, code2=invitation_code_vip2)


@webapp_bp.route("/en/VIP")
def VIP_check_en():
    if current_user.is_authenticated:
        if current_user.vip1 == 'yes':
            if current_user.vip2 == 'yes':
                flash('You are VIP2 user, we have unlocked VIP2 contents for you!', 'success')
                return redirect(url_for('webapp.welcome'))
            else:
                flash('You are VIP1 user, we have unlocked VIP1 contents for you!', 'success')
                return render_template('temporary_vip.html', title = 'Get free VIP', lang = 'en')
        else:
            flash('You are currently not a VIP. Get your temporary VIP here!', 'success')
            return render_template('temporary_vip.html',title = 'Get free VIP', lang = 'en')
    else:
        flash("You haven't login yet, please login first", "warning")
        return redirect(url_for("user.login_en"))


@webapp_bp.route("/cn/VIP")
def VIP_check_cn():
    if current_user.is_authenticated:
        if current_user.vip1 == 'yes':
            if current_user.vip2 == 'yes':
                flash('您是VIP2用户, 我们已经为您解锁了全部的VIP2内容！', 'success')
                return redirect(url_for('webapp.welcome'))
            else:
                flash('您是VIP1用户, 我们已经为您解锁了全部的VIP1内容！,' 'success')
                return render_template('temporary_vip.html', title= '获得免费VIP', lang='cn')
        else:
            flash('您目前还不是VIP用户. 在这里可以获取您的临时VIP!', 'success')
            return render_template('temporary_vip.html', title = '获得免费VIP', lang= 'cn')
    else:
        flash('您目前还没有登录，请首先登录或者注册！', 'warning')
        return redirect(url_for("user.login_cn"))


@webapp_bp.route("/buy_vip")
def buy_vip():
    return render_template('price.html',)

@webapp_bp.route("/about")
def about():
    return render_template('price.html')

@webapp_bp.route("/alipay_vip1")
def alipay_vip1():
    return render_template('alipay_vip1.html')

@webapp_bp.route("/alipay_vip1&2")
def alipay_vip12():
    return render_template('alipay_vip12.html')




