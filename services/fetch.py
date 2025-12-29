import feedparser


def fetch_elementy_articles():
    _feed = feedparser.parse("https://elementy.ru/rss/news")
    save_new_articles(_feed)


def fetch_nasa_articles():
    _feed = feedparser.parse("https://www.nasa.gov/news-release/feed/")
    save_new_articles(_feed)
