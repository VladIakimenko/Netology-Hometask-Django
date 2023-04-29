from django.shortcuts import render
from django.http import HttpResponse
import re

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def recipe_view(request, dish):
    servings = request.GET.get('servings', '1')

    if not re.match(r"^\d+$", servings):
        return HttpResponse(f'Incorrect servings: {servings}<br>'
                            f'Must be a non-negative integer.')
    return render(
        request,
        template_name='calculator/index.html',
        context={'recipe': {key: (value * int(servings)) for key, value in DATA[dish].items()}}
    )
