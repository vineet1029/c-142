from flask import Flask , jsonify, request
import csv
from storage import all_articles,liked_articles,not_liked_articles
from demographic_filtering import output
from content_filtering import getRecommendations

app = Flask(__name__)

@app.route("/get-articles")

def get_articles():

    articles_data = {
        "title": all_articles[0][12],
    }
    return jsonify({
        "data": all_articles[0],
        "status": "success"
    })

@app.route("/liked-articles", methods = ["POST"])

def liked_articles():
    articles = all_articles[0]
    liked_articles.append(articles)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }),201

@app.route("/unliked-articles", methods = ["POST"])

def unliked_articles():
    articles = all_articles[0]
    all_articles.pop(0)
    not_liked_articles.append(articles)
    return jsonify({
        "status": "success"
    }),201
@app.route('/popular-articles')
def popularA_articles():
    articleData = []
    for article in output:
        d = {
            'url': article[0],
            'title': article[1],
            'text': article[2],
            'lang': article[3],
            'total_events': article[4]
        }
        articleData.append(d)
    return jsonify({
        'data': articleData,
        'status': 'success'
    }), 200
@app.route('/recommended-articles')
def recommendedArticles():
    allRecommended = []
    for likedArticle in liked_articles:
        output = getRecommendations(likedArticle[4])
        for data in output:
            allRecommended.append(data)
    import itertools
    allRecommended.sort()
    allRecommended = list(allRecommended for allRecommended,_ in itertools.groupby(allRecommended))
    articleData = []
    for recommended in allRecommended:
        d = {
            'url': recommended[0],
            'title': recommended[1],
            'text': recommended[2],
            'lang': recommended[3],
            'total_events': recommended[4]
        }
        articleData.append(d)
    return jsonify({
        'data': articleData,
        'status': 'success'
    }), 200
if __name__ == "__main__":
    app.run()