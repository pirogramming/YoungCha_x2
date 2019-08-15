import json

from django.shortcuts import render, redirect
from accounts.models import UserHistory, User
from data.data_excel import get_data_json

from .models import CoName
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
        name = "삼성전자"
    elif(sector == "pharma"):
        name = "신라젠"
    elif(sector == "media"):
        name = "NAVER"
    else:
        name = "현대차"
    x = get_data_json(name)
    x = json.loads(x)



    # for i in y:
    #     if name in i:
    #         pass

    price = []
    for i in x:
        price.append(i[1])

    price_result = []

    for i in range(0, 10, 2):
        for j in range(5):
            (price[i+1]-price[i])/10

    # return render(request, "data/trading_game.html", {'data': price, 'name': name, 'ceed': ceed})
    return render(request, "data/trading_game.html", {'data': price, 'name': name, 'ceed': ceed, 'sector':sector})


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

