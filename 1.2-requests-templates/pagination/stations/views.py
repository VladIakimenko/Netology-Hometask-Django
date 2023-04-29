import csv

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse


with open(settings.BUS_STATION_CSV, 'rt', encoding='UTF-8') as sourcefile:
    reader = csv.reader(sourcefile)
    next(reader)
    DATA = [{'name': row[1], 'street': row[4], 'district': row[6]} for row in reader]


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_num = request.GET.get('page', "1")
    try:
        assert(int(page_num) == float(page_num) and int(page_num) > 0)
        page_num = int(page_num)
    except (AssertionError, ValueError) as e:
        return HttpResponse(f'Incorrect page {page_num}!<br>Must be a postive integer.')
        
    paginator = Paginator(DATA, 10)
    page = paginator.get_page(page_num)

    context = {
        'page': page
    }
    return render(request, 'stations/index.html', context)
