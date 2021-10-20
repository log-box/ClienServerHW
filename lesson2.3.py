"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
YAML-формата.
"""
import yaml

DATA_TO_YAML = {
    'list': [1, 'b'],
    'int': 123,
    1:1,
    'dict': {
        '1а': 111,
        '1б': 222,
        '1в': 333,
        '12':2
    }
}

with open('test.yaml', 'w', encoding='utf-8') as yaml_file:
    yaml.dump(DATA_TO_YAML, yaml_file, default_flow_style=False, allow_unicode=True)

with open('test.yaml', 'r', encoding='utf8') as yaml_file:
    yaml_data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    key_errors = 0
    data_errors = 0
    for key, value in DATA_TO_YAML.items():
        if key in yaml_data:
            print(f'[OK] key {key} is in original dict')
            if yaml_data[key] == DATA_TO_YAML[key]:
                print(f'[OK] Data on key {key} is equal to original data')
                print('----------------------')
            else:
                print(f'[ERR] Data on key {key} is not equal to original data')
                print('----------------------')
                data_errors += 1
        else:
            print(f'[ERR] key {key} is not in original dict')
            print('----------------------')
            key_errors += 1
    if (key_errors + data_errors) == 0:
        print('[OK] There no Errors during save and load data to YAML file')
    else:
        print(f'[ERR] There {key_errors} key errors' if key_errors > 0 else '')
        print(f'[ERR] There {data_errors} data errors' if data_errors > 0 else '')
