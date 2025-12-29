from viewer.models import Article
from dateutil import parser
import feedparser


def save_new_articles(feed):
    """Saves new articles to the database.

    Checks the GUID against the episodes currently stored in the
    database. If not found, then a new `Article` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    channel_title = feed.channel.title
    channel_image = feed.channel.get("image", None)

    for item in feed.entries:
        __guid = item.get("guid", item.link)
        if not Article.objects.filter(guid=__guid).exists():
            article = Article(
                title=item.title,
                body=item.description,
                link=item.link,
                image=channel_image,
                guid=__guid,
                pub_date=parser.parse(item.published),
            )
            article.save()


def fetch_4pda_articles():
    _feed = feedparser.parse("https://4pda.to/feed/")
    save_new_articles(_feed)
