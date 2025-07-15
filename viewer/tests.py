from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Article


class ArticleTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="My Awesome article",
            body="Look mom, I'm road kill!",
            pub_date=timezone.now(),
            link="https://acme.show.com",
            image="https://image.acme.com",
            guid="de194720-7b4c-49e2-a05f-432436d3fetr",
        )

    def test_article_content(self):
        self.assertEqual(self.article.body, "Look mom, I'm road kill!")
        self.assertEqual(self.article.link, "https://acme.show.com")
        self.assertEqual(
            self.article.guid, "de194720-7b4c-49e2-a05f-432436d3fetr"
        )

    def test_article_str_representation(self):
        self.assertEqual(
            str(self.article), "My Awesome article"
        )

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "Reader rss")
