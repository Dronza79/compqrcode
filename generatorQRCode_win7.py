import csv
import os

import qrcode
import qrcode.image.svg as fac

factory = fac.SvgPathImage
qr = qrcode.QRCode(version=3)

while True:
    data = []
    FILENAME = 'данные вставлять сюда' + '.csv'
    try:
        with open(FILENAME, 'r', newline='') as file:
            csv_reader = csv.reader(file, delimiter=';', quotechar='|')
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        new_f = open(FILENAME, 'w')
        new_f.close()
        print(f'Надо заполнить файл <<{FILENAME}>>')
        cho = input('Продолжить? д/н... ')
        if cho == 'н':
            break
        continue
    print('Нажмите кнопку:')
    choice = input('1 - для создание папок;\n2 - для создания QRCode;\nлюбая цифра - выход из программы: ')
    if choice == '1':
        SUBSTATION = input('Введите название главной папки: ')
        os.mkdir(SUBSTATION)
        for folder in data:
            os.mkdir(f'{SUBSTATION}/{folder[1]}-{folder[0]}')
    elif choice == '2':
        if not os.path.exists('QRCode'):
            os.mkdir('QRCode')
        try:
            for obj in data:
                print(obj)
                svg = qrcode.make(f'{obj[2]}', image_factory=factory)
                qr.add_data(f'{obj[2]}')
                svg.save(f'QRCode/{obj[1]}-{obj[0]}.svg')
        except IndexError:
            print(f'Вы не пересохранили файл <<{FILENAME}>>, отсутствуют ссылки у папок.')
            print(f'пересохраните файл и нажмите кнопку...')
            symb = input('Продолжить? д/н ')
            if symb == 'н':
                break
    else:
        break
