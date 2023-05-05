from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    name = models.CharField(max_length=200, verbose_name='наименование', null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='цена', null=False, blank=False)
    image = models.CharField(max_length=200, verbose_name='изображение', null=False, blank=False)
    release_date = models.DateField(verbose_name='дата выпуска', null=True, blank=True)
    lte_exists = models.BooleanField(verbose_name='LTE в наличии', blank=True, null=True)
    slug = models.SlugField(max_length=200, verbose_name='slug', unique=True, null=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
