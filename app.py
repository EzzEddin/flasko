import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:' + os.getenv('MYSQL_PASSWORD') + '@localhost:3306/flaskapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True, nullable=False)
    content = db.Column(db.VARCHAR, index=True, nullable=False)
    published = db.Column(db.Boolean, default=False)


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Article=Article)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ArticleForm()
    if form.validate_on_submit():
        old_title = session.get('title')
        if old_title is not None and old_title == form.title.data:
            flash("Looks like you wrote an article with the same title!")
        session['title'] = form.title.data
        session['content'] = form.content.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form)
