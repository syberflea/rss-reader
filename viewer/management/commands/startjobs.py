import logging

from django.conf import settings
from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from viewer.models import Article


logger = logging.getLogger(__name__)


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
                pub_date=parser.parse(item.published)
            )
            article.save()


def fetch_elementy_articles():
    _feed = feedparser.parse("https://elementy.ru/rss/news")
    save_new_articles(_feed)


def fetch_nasa_articles():
    _feed = feedparser.parse("https://www.nasa.gov/news-release/feed/")
    save_new_articles(_feed)


def fetch_4pda_articles():
    _feed = feedparser.parse("https://4pda.to/feed/")
    save_new_articles(_feed)


def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_elementy_articles,
            trigger="interval",
            minutes=2,
            id="Элементы: новости науки",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Elements.")

        scheduler.add_job(
            fetch_4pda_articles,
            trigger="interval",
            minutes=2,
            id="RSS-лента 4PDA",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: 4PDA.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
