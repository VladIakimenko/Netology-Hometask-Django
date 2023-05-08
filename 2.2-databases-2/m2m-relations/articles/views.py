from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    context = {
        'object_list': Article.objects.all().prefetch_related('scopes')
    }
    return render(request, template, context)
