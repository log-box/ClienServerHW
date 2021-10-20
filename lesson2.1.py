"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV.
"""

import csv
import re
from pathlib import Path
from chardet import detect

os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
main_data = []

FILES_COUNT = len(sorted(Path('.').glob('info_*.txt')))
FILES_START = int(re.findall(r'(\d)', str(sorted(Path('.').glob('info_*.txt'))[0]))[0])


def get_data():
    for i in range(FILES_START, FILES_COUNT + 1):
        with open(f'info_{i}.txt', 'rb') as test:
            content = test.read()
        ENCODING = detect(content)['encoding']
        with open(f'info_{i}.txt', 'r', encoding=ENCODING) as file:
            for line in file:
                if re.findall(r'Изготовитель системы:\s+(\w+)', line):
                    os_prod_list.extend(re.findall(r'Изготовитель системы:\s+(\w+)', line))
                if re.findall(r'Название ОС:\s+(\w+)', line):
                    os_name_list.extend(re.findall(r'Название ОС:\s+(\w+)', line))
                if re.findall(r'Код продукта:\s+(\w+)', line):
                    os_code_list.extend(re.findall(r'Код продукта:\s+(\w+)', line))
                if re.findall(r'Тип системы:\s+(\w+)', line):
                    os_type_list.extend(re.findall(r'Тип системы:\s+(\w+)', line))
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for i in range(0, FILES_COUNT):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])
    return main_data


def write_csv_file(file_name):
    try:
        with open(f'{file_name}.csv', 'w') as file:
            file_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            file_writer.writerows(get_data())
        print(f'File "{file_name}.csv" was successful created')
    except Exception:
        print('Something gone wrong... ERROR')


write_csv_file('test_csv_file')
# print(get_data())
