import csv
import os

import qrcode
import qrcode.image.svg as fac

factory = fac.SvgPathImage
qr = qrcode.QRCode(version=1)
filename = 'данные вставлять сюда' + '.csv'


def check_in_data(file):
    data_list = []
    try:
        with open(file, 'r', newline='') as f:
            csv_reader = csv.reader(f, delimiter=';', quotechar='|')
            for row in csv_reader:
                if not all(row):
                    continue
                data_list.append(row)
    except FileNotFoundError:
        new_f = open(file, 'w')
        new_f.close()
    return data_list


SUBSTATION = ''
INSTRUCT = (
    f'\nИНСТРУКЦИЯ:\nПри запуске программы создается файл >>{filename}<< в той же папке, где находится программа.\n'
    f'Для работы программы необходимо открыть и заполнить файл >>{filename}<<, где:\n- первый столбец - это номер '
    f'конструктива;\n- второй столбец - это заводской номер ячейки;\n- третий - ссылка сервера на папку (заполняется '
    f'на втором этапе работы программы).\nЗаполнив файл >>{filename}<< необходимо его пересохранить, выбрав тип '
    f'файла "CSV (разделители - запятые)",\nно не закрывать, иначе удалятся нули в начале заводских номеров.\n'
    f'При указании названия главной папки избегать символов, не используемых при формировании названия папок такие '
    f'как \ / : * ? » " < > |, а также специальные символы и пробелы\n'
    f'На вопросы положительно можно отвечать любой буквой, отрицательно - либо русской "н", '
    f'либо английской "n".\n'
)
print(INSTRUCT)
while True:
    data = check_in_data(filename)
    if not data:
        print(f'Надо заполнить файл >>{filename}<<')
        cho = input('Продолжить? д/н... ')
        if cho in 'нn':
            break
        continue
    print('Выберите действие нажав клавишу:')
    choice = input('1 - для создание папок;\n2 - для создания QRCode;\n3 - инструкция работы программы;\nлюбая цифра - '
                   'выход из программы: ')
    if choice == '1':
        SUBSTATION = input('Введите название главной папки: ')
        os.mkdir(SUBSTATION)
        data = check_in_data(filename)
        for folder in data:
            os.mkdir(f'{SUBSTATION}/{folder[1]}-{folder[0]}')
        print('\nВыполнено...\n')
    elif choice == '2':
        if not os.path.exists(f'{SUBSTATION}/QRCode'):
            os.mkdir(f'{SUBSTATION}/QRCode')
        data = check_in_data(filename)
        try:
            for obj in data:
                print(obj, f'{SUBSTATION}/QRCode/{obj[1]}-{obj[0]}.svg')
                svg = qrcode.make(f'{obj[2]}', image_factory=factory)
                qr.add_data(f'{obj[2]}')
                svg.save(f'{SUBSTATION}/QRCode/{obj[1]}-{obj[0]}.svg')
        except IndexError:
            print(f'\nВы не пересохранили файл >>{filename}<<, отсутствуют ссылки у папок.')
            print(f'Пересохраните файл и нажмите любую кнопку...')
            cho = input('Продолжить? д/н ')
            if cho in 'nн':
                break
        else:
            print('\nВыполнено...\n')
    elif choice == '3':
        print(INSTRUCT)
    else:
        break
