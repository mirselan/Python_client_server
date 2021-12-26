"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но отерыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""

from chardet.universaldetector import UniversalDetector

# Создание файла и запись в него строк:

strings = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as f:
    for line in strings:
        f.write(f'{line}\n')

# кодировка файла по умолчанию:

detector = UniversalDetector()
with open('test_file.txt', 'rb') as t_f:
    for i in t_f:
        detector.feed(i)
        if detector.done:
            break
    detector.close()
print(f"Кодировка файла по умолчанию: {detector.result['encoding']}")

# открытие файла в в формате Unicode:

with open('test_file.txt', 'r', encoding=detector.result['encoding']) as f:
    text = f.read()
print(f'Файл в правильной кодировке: \n{text}')
