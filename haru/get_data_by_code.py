import requests
from bs4 import BeautifulSoup as BS


def get_real_time(code):
    response = requests.get('https://finance.naver.com/item/main.nhn?code=%s' % code)

    html = response.text

    soup = BS(html, 'html.parser')
    real_time_data_list = []
    #print(soup)
    for tag in soup.select('div[class=rate_info]'):
        x = tag.text.split()
        x_ = [x[2], x[7], x[6]]
        real_time_data_list.append(x_)

    return real_time_data_list


response = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0')


html = response.text

soup = BS(html, 'html.parser')

tag_list = []
for tag in soup.select('td[class=number]'):
    x = tag.text.split()
    tag_list.append(x[0])


가격 = tag_list[::10]
등락액 = tag_list[1::10]
등락률 = tag_list[2::10]
시가총액 = tag_list[4::10]

이름 = []

for tag in soup.select('td > a'):
    x = tag.text.split()
    if x and len(이름) < 50:
        이름.append(x[0])


response = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=2')


ooo = soup.select('td > a')

코드 = []

for tag in ooo:
    lll = str(tag).find('code=')
    xxx = str(tag)[lll+5:lll+11]
    if not (xxx in 코드):
        코드.append(xxx)

zip_all = list(zip(이름, 코드, 가격, 등락액, 등락률, 시가총액))


print(zip_all)


def get_for_haru():
    response = requests.get('https://finance.naver.com/item/main.nhn?code=005930')

    html = response.text

    soup = BS(html, 'html.parser')

    for tag in soup.select('div[class=today]'):
        x = tag.text.split()

    # 전일 대비 가격이 동일 할 때 나는 오류  해결
    if len(x) != 11:
        return 0

    return str(x[7] + x[8] + x[10])