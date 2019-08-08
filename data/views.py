from django.shortcuts import render, redirect

from haru import get_data_by_code
from .models import ChartData, CoName
from data.data_excel import get_data_json
import json


def home(request):
    kkk = CoName.objects.all()
    if not kkk:
        yyy = '''
        삼성전자
        SK하이닉스
        아모레퍼시픽
        카카오
        NHN
        신라젠
        셀트리온
        LG디스플레이
        하이트진로홀딩스
        삼성SDI
        NAVER
        현대차
        LG화학
        POSCO
        한국전력
        SK
        SK텔레콤
        엔씨소프트
        LG생활건강'''

        for i in yyy.split():
            CoName.objects.create(name=i)

    if request.method == 'POST':
        z = request.POST.get('name')
        url = '%s/' % z
        return redirect(url)
    name = CoName.objects.all()
    return render(request, "data/home.html", {'name': name})


def data_show(request, name):
    x = get_data_json(name)
    x = json.loads(x)
    y = get_data_by_code.zip_all

    for i in y:
        if name in i:
            pass

    price = []
    for i in x:
        price.append(i[1])

    return render(request, "data/new_new_list.html", {'data': price, 'name': name})



def loading(request):
    return render(request, 'data/loading.html')

