import json

from django.shortcuts import render, redirect

from data.data_excel import get_data_json
from data import get_data_by_code
from .models import CoName

import random
from data.yahoofinance_crawling import companyData

ceed_choice = None
sector_choice =None
names1 = ['삼성전자', 'SK하이닉스', 'LG디스플레이', '삼성SDI', '현대차', 'LG화학', 'POSCO','SK', 'SK텔레콤', 'LG생활건강']
names2 = ['신라젠', '셀트리온']
names3 = ['카카오', 'NAVER', 'NHN', '엔씨소프트']
unnamed = ['아모레퍼시픽', '하이트진로홀딩스', '한국전력']

def index(request):
    return render(request, 'data/index.html')

def ready(request):
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
        # url = '%s/' % z
        url = 'ing/'
        global ceed_choice, sector_choice
        ceed_choice = request.POST.get('ceed')
        sector_choice = request.POST.get('sector')
        return redirect(url)
    name = CoName.objects.all()
    return render(request, "data/ready.html", {'name': name, 'ceed':ceed_choice, 'sector': sector_choice})

# def data_show(request, name):
def data_show(request):
    ceed = ceed_choice
    sector = sector_choice
    if(sector == 'jaebol_4'):
        list = names1
    elif(sector == "pharma"):
        list = names2
    elif(sector == "media"):
        list = names3
    # elif(sector == 'faang'):
    #     name = "fb"
    else:
        list = unnamed

    out = random.sample(list, 1)
    # for i in out:

    for j in out:
        name = j
        x = get_data_json(name)
        x = json.loads(x)

        # price = []
        # for k in z:
        #     price.append(k)
        # y = get_data_by_code.zip_all
        price = []
        for i in x:
            price.append(i[1])

    # return render(request, "data/trading_game.html", {'data': price, 'name': name, 'ceed': ceed})
    return render(request, "data/trading_game.html", {'data': price, 'name': name, 'ceed': ceed, 'sector':sector})

def user_result(request):
    if request.method == 'POST':
        user_result = request.POST.get("abc")
        user_result = user_result.split(",") #스플릿 결과는 리스트
        print(user_result)
        user_result[5:] = [sum(list(map(float, user_result[5:])))]
        return render(request, "data/user_result.html", {'user_result': user_result})

def loading(request):
    return render(request, 'data/loading.html')

