import pandas
import json


def get_data_json(name):
    x = pandas.read_excel('excel_files/1.xls', sheet_name='%s' % name)

    price_top = x['최고가(종가)']

    data = []

    for num, i in enumerate(range(len(price_top))):
        _p_ = str(price_top[i])
        _p_ = _p_.split(',')
        _p = ''

        for j in _p_:
            _p += j

        if name == "삼성전자":
            if int(_p) < 100000:
                _p = str(int(_p) * 50)

        if name == 'NAVER':
            if num < 10:
                _p = str(int(_p)*5)

        data.append(int(_p))
    data = json.dumps(list(reversed(data)))

    return data
