from PIL import Image
from flask import Flask, render_template, redirect, session, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
from forms import LoginForm, RegistrationForm, InviteForm, AddCorrespondent, AddIssue, AddNews
from requests import get, delete
import os

from project_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sfdcbmjs146tff42vnbnmsf100b0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_newspaper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#
link_dict = {'index': 'Главная', 'columns': 'Рубрики', 'correspondents': 'Корреспонденты газеты',
             'newspaper_issues': 'Выпуски газеты'}


def cut_image(image_path):
    original_image = Image.open(image_path)
    width, height = original_image.size
    resized_image = original_image.crop(width, width * 3 // 4)
    resized_image.save(image_path)


# Main page
@app.route('/')
@app.route('/index')
def index():
    slides = Slide.query.filter_by(visible=True).all()
    news_list = News.query.all()
    all_news_text = {}
    for news in news_list:
        with open(news.text_path, 'r') as text:
            all_news_text[news.id] = text.read()
            text.close()
    return render_template('index.html', title='В десяточку', slides=slides,
                           link_dict=link_dict, news_list=news_list, all_news_text=all_news_text, name='index')


# Sign-in page
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if 'username' in session:
        return redirect('/index')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            login = form.login.data
            password = form.password.data
            exists = Admin.query.filter_by(login=login, password=password).first()
            if exists:
                session['username'] = login
                session['user_id'] = exists.id
                return redirect('/index')
            else:
                return redirect('/login')
        return render_template('login.html', title='Авторизация', form=form,
                               link_dict=link_dict, name='')


# Registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if 'username' in session:
        pass
        session.pop('username', 0)
        session.pop('user_id', 0)

    check_form = InviteForm()
    if check_form.validate_on_submit():
        if check_form.invite.data in Invite.query.all():
            reg_form = RegistrationForm()
            if reg_form.validate_on_submit():
                # Check for the existence of the user in db
                user = Admin.query.filter_by(login=reg_form.login.data).first()
                if not user:
                    # Create new user
                    new_user = Admin(login=reg_form.login.data, name=reg_form.name.data,
                                     surname=reg_form.surname.data, email=reg_form.email.data,
                                     password=reg_form.password.data)
                    db.session.add(new_user)
                    db.session.commit()
                    session['username'] = new_user.login
                    session['user_id'] = new_user.id
                    return redirect('/index')
                else:
                    return render_template('error_page.html', title='Ошибка', error='Такой пользователь уже существует',
                                           link_dict=link_dict, name='')
            return render_template('registration.html', title='Регистрация', form=reg_form,
                                   link_dict=link_dict, name='')
        else:
            return render_template('error_page.html', title='Ошибка', error='Неверный код',
                                   link_dict=link_dict, name='')
    return render_template('invite_check.html', title='Проверка кода-приглашения', form=check_form,
                           link_dict=link_dict, name='')


# Logout
@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


# Downloading
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'issues', 'files'), filename)


# Columns page
@app.route('/columns', methods=['GET', 'POST'])
def columns():
    pass


# Correspondents page
@app.route('/correspondents', methods=['GET', 'POST'])
def correspondents_list():
    correspondents = Correspondent.query.all()
    length = len(correspondents)
    return render_template('correspondents.html', title='Корреспонденты', correspondents=correspondents,
                           link_dict=link_dict, name='correspondent', length=length)


# Newspaper issues page
@app.route('/newspaper_issues', methods=['GET', 'POST'])
def newspaper_issues():
    issues = Issue.query.all()
    length = len(issues)
    return render_template('newspaper_issues.html', title='Выпуски газеты', issues=issues,
                           link_dict=link_dict, name='newspaper_issues', length=length)


# Success page
@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html', title='Успешно',
                           link_dict=link_dict, name='')


# Admin_page
@app.route('/administration', methods=['GET', 'POST'])
def administration():
    return render_template('administration.html', title='Администрирование',
                           link_dict=link_dict, name='')


# History of admin's actions
@app.route('/actions', methods=['GET', 'POST'])
def actions():
    pass


# News page
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if not session['username']:
        return redirect('/index')
    form = AddNews()
    if form.validate_on_submit():
        if form.image:
            try:
                image_id = News.query.count() + 1
                image_name = os.path.join(app.config['UPLOAD_FOLDER'], 'images',
                                          'ni_' + str(image_id) + '.jpg')
                form.image.data.save(image_name)
            except Exception as e:
                return render_template('error_page.html', title='Ошибка', error=e,
                                       link_dict=link_dict, name='')

        try:
            text_id = News.query.count() + 1
            text_path = os.path.join(app.config['UPLOAD_FOLDER'], 'news',
                                     'news_' + str(text_id) + '.txt')
            form.text_file.data.save(text_path)
        except Exception as e:
            return render_template('error_page.html', title='Ошибка', error=e,
                                   link_dict=link_dict, name='')

        # Add new correspondent in db
        news = News(heading=form.heading.data, text_path=text_path, image_path=image_name)
        db.session.add(news)
        db.session.commit()
        return redirect('/success')
    return render_template('add_news.html', title='Добавить новость', form=form,
                           link_dict=link_dict, name='')


# Add correspondent
@app.route('/add_correspondent', methods=['GET', 'POST'])
def add_correspondent():
    if not session['username']:
        return redirect('/index')
    form = AddCorrespondent()
    if form.validate_on_submit():
        correspondent = Correspondent.query.filter_by(name=form.name.data, surname=form.surname.data).first()
        if not correspondent:
            try:
                image_id = Correspondent.query.count() + 1
                image_name = os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pictures',
                                          'corr_' + str(image_id) + '.jpg')
                form.image.data.save(image_name)
                # cut_image(image_name)
            except Exception as e:
                return render_template('error_page.html', title='Ошибка', error=e,
                                       link_dict=link_dict, name='')

            # Add new correspondent in db
            new_correspondent = Correspondent(name=form.name.data, surname=form.surname.data, photo=image_name,
                                              description=form.description.data)
            db.session.add(new_correspondent)
            db.session.commit()
            return redirect('/success')
        else:
            return render_template('error_page.html', title='Ошибка', error='Такой корреспондент уже добавлен',
                                   link_dict=link_dict, name='correspondent')
    return render_template('add_correspondent.html', title='Добавить корреспондента', form=form,
                           link_dict=link_dict, name='')


# Add issue
@app.route('/add_issue', methods=['GET', 'POST'])
def add_issue():
    if not session['username']:
        return redirect('/index')
    form = AddIssue()
    if form.validate_on_submit():
        # Save issue
        try:
            file_id = Issue.query.count() + 1
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 'issues', 'files', 'issue_' + str(file_id) + '.pub')
            with open(filename, 'wb') as file:
                file.write(form.file.data.read())
                file.close()
        except Exception as e:
            return render_template('error_page.html', title='Ошибка', error=e,
                                   link_dict=link_dict, name='correspondent')

        # Save cover of issue
        try:
            cover_name = os.path.join(app.config['UPLOAD_FOLDER'], 'issues', 'cover', 'cover_' + str(file_id) + '.jpg')
            with open(cover_name, 'wb') as file:
                file.write(form.cover.data.read())
                file.close()
        except Exception as e:
            return render_template('error_page.html', title='Ошибка', error=e,
                                   link_dict=link_dict, name='correspondent')

        # Add new issue in db
        new_issue = Issue(cover=cover_name, filename=filename, description=form.description.data)
        db.session.add(new_issue)
        db.session.commit()
        return redirect('/success')
    return render_template('add_issue.html', title='Загрузить выпуск', form=form,
                           link_dict=link_dict, name='correspondent')


if __name__ == '__main__':
    db.create_all()
    app.run(port=8080, host='127.0.0.1')
