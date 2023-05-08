from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):
    name = models.CharField(max_length=30, verbose_name='Тематический раздел', unique=True)
    articles = models.ManyToManyField(Article, through='ArticleScope')

    class Meta:
        verbose_name = 'тематический раздел'
        verbose_name_plural = 'разделы'

    def __str__(self):
        return self.name


class ArticleScope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False, verbose_name='основной')

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        unique_together = ('article', 'scope')

    def __str__(self):
        return f'{self.article.title} - {self.scope.name}'