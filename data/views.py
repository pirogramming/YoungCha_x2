import json
import random

from django.shortcuts import render, redirect
from accounts.models import UserHistory, User
from data.data_excel import get_data_json

from .models import CoName, CoData
from operator import itemgetter


ceed_choice = None
sector_choice =None

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

    CoData_instance = CoData.objects.all()
    CoName_instance = CoName.objects.all()
    if not CoData_instance:
        for i in CoName_instance:
            CoData.objects.create(name=i, data=get_data_json("%s" % i.name))

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
    names1 = ['삼성전자', 'SK하이닉스', 'LG디스플레이', '삼성SDI', '현대차', 'LG화학', 'POSCO', 'SK', 'SK텔레콤', 'LG생활건강']
    names2 = ['신라젠', '셀트리온']
    names3 = ['카카오', 'NAVER', 'NHN', '엔씨소프트']
    unnamed = ['아모레퍼시픽', '하이트진로홀딩스', '한국전력']
    ceed = ceed_choice
    sector = sector_choice
    COMPANY_CODE_NAMES_MAPPING = {
        'jaebol_4': names1,
        'pharma': names2,
        'media': names3
    }
    names = COMPANY_CODE_NAMES_MAPPING.get(sector, unnamed)
    name = random.sample(names)

    x = CoData.objects.filter(name_id=name)[0].data

    x = json.loads(x)

    print(x)

    # for i in y:
    #     if name in i:
    #         pass

    # return render(request, "data/trading_game.html", {'data': price, 'name': name, 'ceed': ceed})
    return render(request, "data/trading_game.html", {'data': x, 'name': name, 'ceed': ceed, 'sector':sector})


def user_result(request):
    if request.method == 'POST':
        user_result = request.POST.get("abc")
        user_result = user_result.split(",") #스플릿 결과는 리스트
        print(user_result)

        user_instance = User.objects.filter(id=request.user.id)[0]
        if user_result[3] != '0':
            UserHistory.objects.create(
                user=user_instance,
                stock_name=user_result[0],
                rate_of_return=user_result[1],
                total_assets=user_result[2],
                amount_of_asset_change=user_result[3],
                trade_numbers=user_result[4],
                john_bur_term=user_result[5],
            )
            user_result[5:] = [sum(list(map(float, user_result[5:])))]

        else:
            UserHistory.objects.create(
                user=user_instance,
                stock_name=user_result[0],
                rate_of_return=0,
                total_assets=user_result[2],
                amount_of_asset_change=0,
                trade_numbers=0,
                john_bur_term=0,
            )
            user_result[5:] = ['0']

        return render(request, "data/user_result.html", {'user_result': user_result})


def loading(request):
    return render(request, 'data/loading.html')


def leader_board(request):
    leader_board_data = User.objects.all()

    leader_board_data_list = []
    for i in leader_board_data:
        li = []
        for j in UserHistory.objects.filter(user_id=i.id):
            li.append(j.rate_of_return)

        if li:
            max_rate = max(li)
            leader_board_data_list.append([i, float(max_rate)])
        else:
            max_rate = 0
            leader_board_data_list.append([i, float(max_rate)])
    leader_board_data_list.sort(key=itemgetter(1), reverse=True)
    print(leader_board_data_list)
    return render(request, 'data/leader_board.html', {'leader_board_data': leader_board_data_list})

