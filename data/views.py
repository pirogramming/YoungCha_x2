import json
import random

from django.shortcuts import render, redirect
from accounts.models import UserHistory, User, Profile
from data.data_excel import get_data_json

from .models import CoName, CoData
from operator import itemgetter
from data.csvtodb import adjclose_list

ceed_choice = None
sector_choice =None


def index(request):
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
        LG생활건강
        '''

        for i in yyy.split():
            CoName.objects.create(name=i)

    CoData_instance = CoData.objects.all()
    CoName_instance = CoName.objects.all()
    if not CoData_instance:
        for i in CoName_instance:
            CoData.objects.create(name=i, data=get_data_json("%s" % i.name))
        staples = ['GIS', 'HRL', 'K', 'KHC', 'KO', 'MCD', 'MDLZ', 'MO', 'PEP', 'SBUX', 'STZ', 'WMT']
        giants = ['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX', 'MSFT']
        for item in staples:
            if item not in CoName_instance:
                CoName.objects.create(name = item)
            if item not in CoData_instance:
                CoData.objects.create(name = CoName.objects.get(name=item), data = adjclose_list(item)['Adj Close'])
        for item in giants:
            if item not in CoName_instance:
                CoName.objects.create(name = item)
            if item not in CoData_instance:
                CoData.objects.create(name = CoName.objects.get(name=item), data = adjclose_list(item)['Adj Close'])
    return render(request, 'data/index.html')


def ready(request):
    if request.method == 'POST':
        # z = request.POST.get('name')
        # url = '%s/' % z
        url = 'ing/'
        global ceed_choice, sector_choice
        ceed_choice = request.POST.get('ceed')
        sector_choice = request.POST.get('sector')
        return redirect(url)
    # name = CoName.objects.all()
    try:
        user = Profile.objects.filter(user_id=request.user.id)[0]
        wallet_3 = format(user.wallet, ",")
        return render(request, "data/ready.html", {'ceed':ceed_choice, 'sector': sector_choice, 'user_wallet': wallet_3})
    except Exception:
        return render(request, "data/ready.html", {'ceed':ceed_choice, 'sector': sector_choice, 'user_wallet': 0})


# def data_show(request, name):
def data_show(request):
    jaebol = ['삼성전자', 'SK하이닉스', 'LG디스플레이', '삼성SDI', '현대차', 'LG화학', 'POSCO', 'SK', 'SK텔레콤', 'LG생활건강']
    pharma = ['신라젠', '셀트리온']
    media = ['카카오', 'NAVER', 'NHN', '엔씨소프트']
    unnamed = ['아모레퍼시픽', '하이트진로홀딩스', '한국전력']
    staples = ['GIS', 'HRL', 'K', 'KHC', 'KO', 'MCD', 'MDLZ', 'MO', 'PEP', 'SBUX', 'STZ', 'WMT']
    giants = ['AAPL', 'AMZN', 'FB', 'GOOG', 'NFLX', 'MSFT']

    ceed = int(ceed_choice)*10000
    user_instance = Profile.objects.filter(user_id=request.user.id)[0]
    user_instance.wallet -= ceed
    user_instance.save()

    sector = sector_choice

    COMPANY_CODE_NAMES_MAPPING = {
        'jaebol': jaebol,
        'pharma': pharma,
        'media': media,
        'staples': staples,
        'giants': giants,
    }
    names = COMPANY_CODE_NAMES_MAPPING.get(sector, unnamed)
    name = random.sample(names, 1)[0]
    x = CoData.objects.filter(name_id=name)[0].data
    x = json.loads(x)
    index = 0
    is_ing = 'true'
    if request.method == 'POST':
        aa = request.POST.get("value")
        index += int(aa)
        if index == 10:
            is_ing = 'false'
        print(index)
        print(x[index])
        print(is_ing)
        return render(request, "data/trading_game.html", {'data': x[index], 'name': name, 'ceed': ceed, 'sector':sector, 'is_ing': is_ing})
    else:
        return render(request, "data/trading_game.html", {'data': x[index], 'name': name, 'ceed': ceed, 'sector':sector, 'is_ing': is_ing})

def showdb(request):
    giants = ['AAPL', 'AMZN', 'FB', 'GOOG', 'MSFT']
    staples = ['GIS', 'HRL', 'K', 'KHC', 'KO', 'MCD', 'MDLZ', 'MO', 'PEP', 'SBUX', 'STZ', 'WMT']
    print('b')
    index = 0
    if request.method == 'POST':
        aa = request.POST.get("value")
        print(aa)
        index += int(aa)
        print(index)
        context = {
            'adjclose': adjclose_json[index],
            'index': index
        }
        jsonctx = json.dumps(context)
        print(jsonctx)
        return HttpResponse(jsonctx, content_type="application/json")
    else:
        print('c')
        context = {
            'adjclose': adjclose_json[index],
            'index': index,
            'ticker': ticker
        }
        return render(request, 'csvdata/showdb.html', context)

def loading(request):
    return render(request, 'data/loading.html')

def leader_board(request):

    sort = request.GET.get('sort', '')
    leader_board_data_list = []

    if sort == 'max_rate' or sort == '':
        leader_board_data = Profile.objects.all()

        for i in leader_board_data:
            li = []
            for j in UserHistory.objects.filter(user_id=i.user_id):
                li.append(j.rate_of_return)

            if li:
                max_rate = max(li)
                leader_board_data_list.append([i.name, float(max_rate)])
            else:
                max_rate = 0
                leader_board_data_list.append([i.name, float(max_rate)])

        leader_board_data_list.sort(key=itemgetter(1), reverse=True)
        user = Profile.objects.filter(user_id=request.user.id)[0]
        wallet_3 = format(user.wallet, ",")
        return render(request, 'data/leader_board.html', {'leader_board_data': leader_board_data_list, "sort": sort, 'user_wallet': wallet_3})

    if sort == "wallet":
        leader_board_data = Profile.objects.all()
        user_data = User.objects.all()
        leader_board_data_list = []

        for i in leader_board_data:
            leader_board_data_list.append([i.name, format(i.wallet, ",")])
            user_data.filter()
        leader_board_data_list.sort(key=itemgetter(1), reverse=True)
        user = Profile.objects.filter(user_id=request.user.id)[0]
        wallet_3 = format(user.wallet, ",")
        return render(request, 'data/leader_board.html', {'leader_board_data': leader_board_data_list, "sort": sort, 'user_wallet': wallet_3})
