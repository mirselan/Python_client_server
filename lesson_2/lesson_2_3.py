"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml

data = {'items': ['monitor', 'notebook', 'smartphone'],
        'items_quantity': 3,
        'items_price': {'monitor': '150€-500€',
                        'notebook': '200€-1500€',
                        'smartphone': '50€-700€'}
        }

with open('file.yaml', 'w', encoding='utf-8') as f_1:
    yaml.dump(data, f_1, default_flow_style=False,
              allow_unicode=True, sort_keys=False)

with open('file.yaml', 'r', encoding='utf-8') as f_2:
    reading_data = yaml.load(f_2, Loader=yaml.SafeLoader)

print(data == reading_data)
