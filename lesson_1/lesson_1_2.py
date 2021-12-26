"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

string_byte_1, string_byte_2, string_byte_3 = b'class', b'function', b'method'

strings_byte_list = [string_byte_1, string_byte_2, string_byte_3]

for i in strings_byte_list:
    print(f'Тип переменной: {type(i)}, содержимое переменной: {i}, \n'
          f'Длинна переменной: {len(i)}.')

