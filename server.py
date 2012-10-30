from flask import Flask, render_template
from flask.ext.pymongo import PyMongo


app = Flask('wordlearn')
mongo = PyMongo(app)


@app.route('/')
def home_page():
    top_words = mongo.db.words.find().sort('occurrences', -1).limit(40)
    return render_template('words_list.html', top_words=top_words)


if __name__ == "__main__":
    app.run()
