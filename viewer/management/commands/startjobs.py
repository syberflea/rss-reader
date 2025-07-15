from turtle import title
from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser

from viewer.models import Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        feed = feedparser.parse("https://elementy.ru/rss/news")
        channel_title = feed.channel.title
        channel_image = feed.channel.image["href"]

        for item in feed.entries:
            __guid = item.get("guid", item.link)
            if not Article.objects.filter(guid=__guid).exists():
                article = Article(
                    title=item.title,
                    body=item.description,
                    link=item.link,
                    image=channel_image,
                    guid=__guid,
                    pub_date=parser.parse(item.published)
                )
                article.save()
