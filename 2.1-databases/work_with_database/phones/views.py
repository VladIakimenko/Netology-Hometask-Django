from django.shortcuts import render, redirect
from phones.models import Phone
from django.forms.models import model_to_dict


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sorting = request.GET.get('sort')
    sort_options = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
        None: 'name',
    }
    phones = Phone.objects.all().order_by(sort_options[sorting])

    template = 'catalog.html'
    context = {
        'phones': phones
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {
        'phone': model_to_dict(Phone.objects.all().filter(slug=slug).get())
    }
    return render(request, template, context)
