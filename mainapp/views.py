import os
import json

dir = os.path.dirname(__file__)

from django.shortcuts import render
from mainapp.models import Poduct, ProductCategory

# Create your views here.
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)

def products(request):
    context = {
        'tittle': "GeekShop",
        'products': Poduct.objects.all(),
        'categories': Poduct.objects.all(),
    }
    file_path = os.path.join(dir,'fixtures/products.json')
    context.update(json.load(open(file_path,encoding='utf-8')))
    return render(request, 'mainapp/products.html', context)


