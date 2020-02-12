from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email


# Form for page for invite check
class InviteForm(FlaskForm):
    invite = PasswordField('Код-приглашение', validators=[DataRequired()])
    submit = SubmitField('Продолжить')


# Form for sig-in page
class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


# Form for registration page
class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Зарегистрироваться')


# Form for adding correspondent
class AddCorrespondent(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    description = TextAreaField('Описание (не обязательно)')
    image = FileField('Загрузите изображение (только .jpg)', validators=[DataRequired()])
    submit = SubmitField('Добавить')


# Form for adding issue
class AddIssue(FlaskForm):
    name = StringField('Название выпуска', validators=[DataRequired()])
    file = FileField('Загрузите выпуск газеты (только .pub)', validators=[DataRequired()])
    cover = FileField('Загрузите обложку выпуска газеты (только .jpg)', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


# Form for adding news
class AddNews(FlaskForm):
    heading = StringField('Название', validators=[DataRequired()])
    text_file = FileField('Загрузите файл .txt с текстом новости', validators=[DataRequired()])
    image = FileField('Загрузите изображение (не обязательно)')
    submit = SubmitField('Добавить')
