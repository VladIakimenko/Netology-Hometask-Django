from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, ArticleScope


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                counter += 1
        if counter != 1:
            arg = (
                'Нельзя пометить больше одного раздела как основной!',
                'Хотя бы один раздел должен быть помечен, как основной!'
            )[counter == 0]
            raise ValidationError(arg)
        return super().clean()


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    extra = 1
    formset = ArticleScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'published_at', 'image')
    inlines = ArticleScopeInline,


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass
