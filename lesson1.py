# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат
# Unicode и также проверить тип и содержимое переменных.
str1 = 'разработка'
str2 = 'сокет'
str3 = 'декоратор'
print(type(str1))
print(type(str2))
print(type(str3))
print(str1)
print(str2)
print(str3)
uni1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
uni2 = '\u0441\u043e\u043a\u0435\u0442'
uni3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
print(type(uni1))
print(type(uni2))
print(type(uni3))
print(uni1)
print(uni2)
print(uni3)
#################################################
# 2. Каждое из слов «class», «function», «method» записать в
# байтовом типе без преобразования в последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.
byte1 = b'class'
byte2 = b'function'
byte3 = b'method'
# byte4 = b'Привет'
print(type(byte1))
print(type(byte2))
print(type(byte3))
print(byte1)
print(byte2)
print(byte3)
print(len(byte1))
print(len(byte2))
print(len(byte3))
#################################################
# 3. Определить, какие из слов «attribute», «класс», «функция»,
# «type» невозможно записать в байтовом типе.
# byte4 = b'функция'
# SyntaxError: bytes can only contain ASCII literal characters.
#################################################
# 4. Преобразовать слова «разработка», «администрирование», «protocol»,
# «standard» из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и
# decode).
str4 = 'разработка'
str5 = 'администрирование'
str6 = 'protocol'
str7 = 'standard'
print(str4.encode().decode())
print(str5.encode().decode())
print(str6.encode().decode())
print(str7.encode().decode())
#################################################
# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в
# строковый тип на кириллице.
import subprocess

ARGS1 = ['ping', 'yandex.ru']
ARGS2 = ['ping', 'youtube.com']

# YA_PING1 = subprocess.Popen(ARGS1, stdout=subprocess.PIPE)
# for line in YA_PING1.stdout:
#     line = line.decode()
#     print(line)
# 64 bytes from yandex.ru (77.88.55.80): icmp_seq=1 ttl=248 time=23.5 ms
#
# 64 bytes from yandex.ru (77.88.55.80): icmp_seq=2 ttl=248 time=22.0 ms
#
# 64 bytes from yandex.ru (77.88.55.80): icmp_seq=3 ttl=248 time=19.6 ms
#
# 64 bytes from yandex.ru (77.88.55.80): icmp_seq=4 ttl=248 time=19.4 ms
#
# 64 bytes from yandex.ru (77.88.55.80): icmp_seq=5 ttl=248 time=24.3 ms
#
# 64 bytes from yandex.ru (77.88.55.80): icmp_seq=6 ttl=248 time=21.1 ms

YA_PING2 = subprocess.Popen(ARGS2, stdout=subprocess.PIPE)
# for line in YA_PING2.stdout:
#     line = line.decode()
#     print(line)

# 64 bytes from lg-in-f190.1e100.net (64.233.165.190): icmp_seq=1 ttl=58 time=28.3 ms
#
# 64 bytes from lg-in-f190.1e100.net (64.233.165.190): icmp_seq=2 ttl=58 time=30.5 ms
#
# 64 bytes from lg-in-f190.1e100.net (64.233.165.190): icmp_seq=3 ttl=58 time=28.0 ms
#
# 64 bytes from lg-in-f190.1e100.net (64.233.165.190): icmp_seq=4 ttl=58 time=29.5 ms
#
# 64 bytes from lg-in-f190.1e100.net (64.233.165.190): icmp_seq=5 ttl=58 time=28.0 ms
#################################################
# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
# программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в
# формате Unicode и вывести его содержимое.

with open('test_file.txt', 'w') as file:
    file.write('сетевое программирование\nсокет\nдекоратор\n')
    print(type(file))
with open('test_file.txt', 'r', encoding='utf8') as file:
    for line in file:
        print(line)
