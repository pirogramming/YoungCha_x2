from django.shortcuts import render
from .get_data_by_code import zip_all, get_for_haru


# Create your views here.


def home(request):
    get_for_haru()
    return render(request, "haru/today.html", {'data': zip_all, 'func': get_for_haru})


def first(request):
    return render(request, 'haru/index.html')

