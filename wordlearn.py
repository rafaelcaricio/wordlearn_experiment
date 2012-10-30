import re
from pymongo import Connection


connection = Connection()
db = connection.wordlearn
db.drop_collection('words')
db.words.ensure_index('word')

def remove_html_tags(content):
    return re.sub('<[^<]+?>', ' ', content)


english_stopwords = set(['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once', 'it\'s', 'you\'re', 'i\'m', 'don\'t','there\'s', 'he\'s', 'she\'s', 'they\'re'])


simple_word = re.compile('^[a-zA-Z`\'-]+$')


def filter_words(sentence):
    words = sentence.split()
    words = [re.sub('[^\w`\'-]+', '', w).lower() for w in words]
    return [word for word in words if not word in english_stopwords and simple_word.match(word)]


def dump_words(words):
    for w in words:
        db.words.update({'word': w}, {'$inc': {'occurrences': 1}}, True)


if __name__ == '__main__':
    from libepub.book import Book
    book = Book('Being_Geek.epub')
    for c in book.chapters[10:]:
        dump_words(filter_words(remove_html_tags(c.content)))

    print 'Top words in this book:'
    for w in db.words.find().sort('occurrences', -1).limit(20):
        print w['word'], w['occurrences']
