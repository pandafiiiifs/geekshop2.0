from django.shortcuts import render
from django.core.paginator import Paginator

from mainapp.models import Product, ProductCategory


# функции = вьюхи = контроллеры
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    context = {'title': 'GeekShop - Каталог', 'categories': ProductCategory.objects.all()}
    if category_id:
        context.update({'products': Product.objects.filter(category_id= category_id)})
    else:
        context.update({'products': Product.objects.all()})
    return render(request, 'mainapp/products.html', context)