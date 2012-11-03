import redis
from flask import Flask, request, render_template

import keys


app = Flask('wordlearn')
db = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        word = request.form['w']
        db.zrem(keys.TOP_WORDS_IN_BOOK, word)
        db.sadd(keys.WORDS_I_KNOW, word)
    top_words = db.zrange(keys.TOP_WORDS_IN_BOOK, 0, 40, desc=True, withscores=True, score_cast_func=int)
    return render_template('words_list.html', top_words=top_words)


if __name__ == "__main__":
    app.run()
