import redis
import keys

from engine import remove_html_tags, filter_words


def dump_words(db, chapter, words):
    for w in words:
        if not db.sismember(keys.WORDS_I_KNOW, w):
            # process new words per chapter
            # if not know this word and is not in the top words yet
            if not db.zrank(keys.TOP_WORDS_IN_BOOK, w):
                db.hincrby(keys.NEW_WORDS_DISTRIBUTION_BY_CHAPTER, keys.CHAPTER_HASH_KEY.format(chapter))

            db.zincrby(keys.TOP_WORDS_IN_BOOK, w)


if __name__ == '__main__':
    from libepub.book import Book

    db = redis.StrictRedis(host='localhost', port=6379, db=0)
    db.delete(keys.WORDS_IN_BOOK)
    db.delete(keys.TOP_WORDS_IN_BOOK)
    db.delete(keys.NEW_WORDS_DISTRIBUTION_BY_CHAPTER)

    book = Book('../Being_Geek.epub')
    for chapter, c in enumerate(book.chapters[1:], 1):
        dump_words(db, chapter, filter_words(remove_html_tags(c.content)))

    print('All words of this book are stored in the database.')

    top_words = db.zrange(keys.TOP_WORDS_IN_BOOK, 0, 20, desc=True, withscores=True, score_cast_func=int)
    for w in top_words:
        print(w)
    print('number of words {:d}'.format(db.zcount(keys.TOP_WORDS_IN_BOOK, '-inf', '+inf')))

    print('\nNumber of new words per chapter:')
    for key, value in sorted([(key, value) for key, value in db.hgetall(keys.NEW_WORDS_DISTRIBUTION_BY_CHAPTER).items()], key=lambda item: item[0]):
        print(key, value)
