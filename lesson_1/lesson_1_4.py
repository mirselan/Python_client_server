"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

str_1, str_2, str_3, str_4 = 'разработка', 'администрирование', 'protocol', 'standard'

strings_list = [str_1, str_2, str_3, str_4]

print('Байтовое представление: ')

bytes_el = []
for i in strings_list:
    byte_el = i.encode('utf-8')
    bytes_el.append(byte_el)
    print(byte_el)

print('Строковое представление: ')

strings_el = []
for i in bytes_el:
    string_el = i.decode('utf-8')
    strings_el.append(string_el)

print(strings_el)
