import pandas
import json


def get_data_json(name):
    x = pandas.read_excel('excel_files/1.xls', sheet_name='%s' % name)

    date = x['년/월/일']
    price_top = x['최고가(종가)']
    price_bottom = x['최저가(종가)']

    data = []

    for num, i in enumerate(range(len(date))):
        _d = str(date[i])
        _d = _d.split('/')
        _d = _d[0] + _d[1] + '01'

        _p_ = str(price_top[i])
        _p_ = _p_.split(',')
        _p = ''

        _pp_ = str(price_bottom[i])
        _pp_ = _pp_.split(',')
        _pp = ''

        for j in _pp_:
            _pp += j

        for j in _p_:
            _p += j

        if name == "삼성전자":
            if int(_p) < 100000:
                _p = str(int(_p) * 50)
            if int(_pp) < 100000:
                _pp = str(int(_pp) * 50)

        if name == 'NAVER':

            if num < 10:
                _p = str(int(_p)*5)

        data.append([str(_d), int(_p), int(_pp)])
    data = json.dumps(list(reversed(data)))

    return data


print(get_data_json('삼성전자'))
