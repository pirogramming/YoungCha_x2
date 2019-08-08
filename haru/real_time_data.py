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



print(get_real_time("005930"))