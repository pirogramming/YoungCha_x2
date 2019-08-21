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
        try:
            CoName_instance.get(name=item)
        except Exception:
            CoName.objects.create(name=item)
        try:
            CoData_instance.get(name=item)
        except Exception:
            CoData.objects.create(name = CoName.objects.get(name=item), data = adjclose_list(item)['Adj Close'])
    for item in giants:
        try:
            CoName_instance.get(name=item)
        except Exception:
            CoName.objects.create(name = item)
        try:
            CoData_instance.get(name=item)
        except Exception:
            CoData.objects.create(name = CoName.objects.get(name=item), data = adjclose_list(item)['Adj Close'])
    return render(request, 'data/index.html')


def ready(request):
    if request.method == 'POST':
        # z = request.POST.get('name')
        # url = '%s/' % z
        url = 'ing/'
        global ceed_choice, sector_choice
        ceed_choice = request.POST.get('ceed')
        try:
            user = Profile.objects.filter(user_id=request.user.id)[0]
        except Exception:
            try:
                user = Profile.objects.filter(user_id=request.user.id)[0]
                wallet_3 = format(user.wallet, ",")

                return render(request, "data/ready.html",
                              {'ceed': ceed_choice, 'sector': sector_choice, 'user_wallet': wallet_3, 'text': text})
            except Exception:
                text = "로그인된 유저만 사용 가능한 기능입니다"
                return render(request, "data/ready.html",
                              {'ceed': ceed_choice, 'sector': sector_choice, 'user_wallet': 0, 'text': text})
        if 0 < int(ceed_choice)*10000 < int(user.wallet):
            sector_choice = request.POST.get('sector')
            return redirect(url)
        else:
            text = "투자금은 0원보다는 크고 현재 자산보다는 작아야 합니다"
            try:
                user = Profile.objects.filter(user_id=request.user.id)[0]
                wallet_3 = format(user.wallet, ",")

                return render(request, "data/ready.html",
                              {'ceed': ceed_choice, 'sector': sector_choice, 'user_wallet': wallet_3, 'text': text})
            except Exception:
                return render(request, "data/ready.html",
                              {'ceed': ceed_choice, 'sector': sector_choice, 'user_wallet': 0, 'text': text})
    # name = CoName.objects.all()
    try:
        user = Profile.objects.filter(user_id=request.user.id)[0]
        wallet_3 = format(user.wallet, ",")

        return render(request, "data/ready.html", {'ceed': ceed_choice, 'sector': sector_choice, 'user_wallet': wallet_3})
    except Exception:
        return render(request, "data/ready.html", {'ceed': ceed_choice, 'sector': sector_choice, 'user_wallet': 0})


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

    # for i in y:
    #     if name in i:
    #         pass

    # return render(request, "data/trading_game.html", {'data': price, 'name': name, 'ceed': ceed})
    return render(request, "data/trading_game.html", {'data': x, 'name': name, 'ceed': ceed, 'sector':sector})


def user_result(request):
    if request.method == 'POST':

        user_result = request.POST.get("abc")
        user_result = user_result.split(",") #스플릿 결과는 리스트
        user_instance = User.objects.filter(id=request.user.id)[0]
        user_instance.wallet += user_result

        user_instance.save()
        if user_result[3] != '0':
            UserHistory.objects.create(
                user=user_instance,
                stock_name=user_result["name"], # 0 = name
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

        return render(request, 'data/leader_board.html', {'leader_board_data': leader_board_data_list, "sort": sort})

    if sort == "wallet":
        leader_board_data = Profile.objects.all()
        user_data = User.objects.all()
        leader_board_data_list = []

        for i in leader_board_data:
            leader_board_data_list.append([i.name, i.wallet])
            user_data.filter()
        leader_board_data_list.sort(key=itemgetter(1), reverse=True)

        return render(request, 'data/leader_board.html', {'leader_board_data': leader_board_data_list, "sort": sort})
