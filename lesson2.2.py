"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах.
"""
import json
import datetime

from chardet import detect


def write_order_to_json(item=None, quantity=None, price=None, buyer='anonymous', _date=datetime.date.today()):
    if _date != datetime.date.today():
        try:
            date_obj = datetime.datetime.strptime(_date, '%d.%m.%Y')
            _date = date_obj.date()
        except ValueError:
            print('use date format %d.%m.%Y. Example "31.03.1984"')
            _date = None
    if _date is not None:
        order = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': str(_date)
        }
        with open(f'orders.json', 'rb') as test:
            content = test.read()
        ENCODING = detect(content)['encoding']
        with open('orders.json', 'r', encoding=ENCODING) as json_file:
            _dict = json.load(json_file)
            _dict['orders'].append(order)
        with open('orders.json', 'w', encoding=ENCODING) as json_file:
            json.dump(_dict, json_file, sort_keys=True, indent=4, ensure_ascii=True)
        print(_dict)


write_order_to_json('Tovar1', 5, 1000, 'logbox', '12.0323.1999')
