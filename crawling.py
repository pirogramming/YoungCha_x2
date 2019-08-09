# import requests
# from bs4 import BeautifulSoup as BS
#
#
#
# response = requests.get('https://finance.yahoo.com/quote/005930.KS/history?period1=978274800&period2=1565190000&interval=1mo&filter=history&frequency=1mo')
# # get으로 url에서 html을 긁어온다.
# html = response.text
# # response를 text로 바꿔야한다.
# soup = BS(html, 'html.parser')
# # beautifulsoap가 이용할수 있게 하는거. 앞의 인자는 파싱해주고싶은 인자., 뒤는 'html.parser' html형식으로 파싱
# # print(soup)
#
# for tag in soup.select('#render-target-default > div > div.Pos\(r\).Bgc\(\$bg-content\).Miw\(1007px\).Maw\(1260px\).tablet_Miw\(600px\)--noRightRail.Bxz\(bb\).Bdstartc\(t\).Bdstartw\(20px\).Bdendc\(t\).Bdends\(s\).Bdendw\(20px\).Bdstarts\(s\).Mx\(a\)'):
#     x = tag.text.split()
#     print(x[0])
#
# #
# # soup.select 선택자를 다 모아온다.
#
#
