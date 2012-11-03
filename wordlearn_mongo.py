from pymongo import Connection

from engine import remove_html_tags, filter_words


def dump_words(db, words):
    for w in words:
        db.words.update({'word': w}, {'$inc': {'occurrences': 1}}, True)


if __name__ == '__main__':
    from libepub.book import Book

    connection = Connection()
    db = connection.wordlearn
    db.drop_collection('words')
    db.words.ensure_index([('word', 1), ('occurrences', -1)])

    book = Book('../Being_Geek.epub')
    for c in book.chapters[1:]:
        dump_words(db, filter_words(remove_html_tags(c.content)))

    print('All words of this book are stored in the database.')
