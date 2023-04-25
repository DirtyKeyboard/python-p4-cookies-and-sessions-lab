#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
"""
Each user can view a maximum of three articles before seeing the paywall.

When a user makes a GET request to /articles/<int:id>, the following should happen:

If this is the first request this user has made, set session['page_views'] to an initial value of 0.
Hint: consider using a ternary operator to set this initial value!
For every request to /articles/<int:id>, increment the value of session['page_views'] by 1.
If the user has viewed 3 or fewer pages, render a JSON response with the article data.
If the user has viewed more than 3 pages, render a JSON response including an error message {'message': 'Maximum pageview limit reached'}, and a status code of 401 unauthorized.
An API endpoint at /clear is available to clear your session as needed.
"""
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>', methods=["GET"])
def show_article(id):
    if session.get("page_views") == None:
        session['page_views'] = 1
    else:
        session['page_views'] = session['page_views'] + 1

    v = session.get("page_views")
    if v <= 3:
        resp = Article.query.filter(Article.id == id).first().to_dict()
        return make_response(resp, 200)
    else:
        return make_response({"message": "Maximum pageview limit reached"}, 401)
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
