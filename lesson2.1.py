import csv
import re
from pathlib import Path

os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
main_data = []

FILES_COUNT = len(sorted(Path('.').glob('info_*.txt')))
FILES_START = int(re.findall(r'(\d)', str(sorted(Path('.').glob('info_*.txt'))[0]))[0])


def get_data():
    for i in range(FILES_START, FILES_COUNT + 1):
        with open(f'info_{i}.txt', 'r', encoding='cp1251') as file:
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
    with open(f'{file_name}.csv', 'w') as file:
        file_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in get_data():
            file_writer.writerow(row)

write_csv_file('test_csv_file')
# print(get_data())


