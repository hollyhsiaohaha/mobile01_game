from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask import request
from datetime import datetime


db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://test_user:HollyHsiao89!@127.0.0.1:3306/test"

db.init_app(app)


# 模型( model )定義
class Mobile01(db.Model):
    __tablename__ = 'mobile01'
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    link = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    creator = db.Column(db.String(100), nullable=True)
    feedback = db.Column(db.Integer, nullable=True)

    def __init__(self, article_id, title, link, category, creator, feedback):
        self.article_id = article_id
        self.title = title
        self.link = link
        self.category = category
        self.creator = creator
        self.feedback = feedback


@app.route('/')
def index():
    # db.create_all()
    return 'Connection test ok'


@app.route('/most_feedback')
def most_feedback():
    query = Mobile01.query.order_by(Mobile01.feedback.desc()).first()
    return (jsonify({'article_id':query.article_id, 'title':query.title, 'feedback':query.feedback}))
    
    # try:
    #     query = Mobile01.query.order_by(Mobile01.feedback.desc()).first()
    #     return (jsonify({'article_id':query.article_id, 'title':query.title, 'feedback':query.feedback}))
    # except:
    #     return("error_most_feedback")


# Input article id and search for article information
@app.route('/like_article_title/<like_title>')
def like_article_title(like_title, each_article=None):
    print(like_title)
    search = "%{}%".format(like_title)
    query = Mobile01.query.filter(Mobile01.title.like(search)).all()

    article_list = []
    for each_article in query:
        article_information = dict(article_id=each_article.article_id, title=each_article.title)
        article_list.append(article_information)

    print(article_list)
    search_result = dict(search_result=article_list)
    return (search_result)


# Input article id and search for article information
@app.route('/by_article_id/<int:input_article_id>')
def show_post(input_article_id):
    try:
        query = Mobile01.query.filter_by(article_id=input_article_id).first()
        return (jsonify({'article_id':query.article_id, 'title':query.title, 'link':query.link,  'category':query.category, 'creator':query.creator, 'feedback':query.feedback}))
    except:
        return("The article_id does not exist")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

# TODO: Figure out how to create the Dockerfile
# TODO: Docker-compose