from django.db import models


class Source(models.Model):
    link = models.URLField(
        max_length=200,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        blank=False,
        null=False
    )
    subtitle = models.CharField(
        max_length=200,
        verbose_name='Подзаголовок'
    )
    feed = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации'
    )

    def __str__(self) -> str:
        return self.title


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        blank=False,
        null=False
    )
    body = models.TextField()
    link = models.URLField()
    image = models.URLField(
        'Иконка',
        null=True,
        blank=True
    )
    guid = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    unread = models.BooleanField(
        default=True,
        null=False
    )
    source = models.ForeignKey(
        Source,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Источник',
        help_text='Выберите источник'
    )
    pub_date = models.DateTimeField()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
