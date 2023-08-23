from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    context = {
        'title': 'Test title',
        'username': 'wezxasqw',
        'is_flagged': True
    }
    return render(request, 'products/index.html', context=context)


def products(request: HttpRequest):
    context = {
        'title': 'My products',
        'products': [
            {
                'image': '/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png',
                'title': 'Темно-синие широкие строгие брюки ASOS DESIGN',
                'price': 2890,
                'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.',
            },
            {
                'image': '/static/vendor/img/products/Black-Dr-Martens-shoes.png',
                'title': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
                'price': 13590,
                'description': 'Гладкий кожаный верх. Натуральный материал.',
            },
            {
                'image': '/static/vendor/img/products/Black-Nike-Heritage-backpack.png',
                'title': 'Черный рюкзак Nike Heritage',
                'price': 2340,
                'description': 'Плотная ткань. Легкий материал.',
            },
        ]
    }
    return render(request, 'products/products.html', context=context)
