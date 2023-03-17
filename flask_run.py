import requests
from flask import Flask, render_template, request
import time
from database_pr import Database

from config.settings import DATABASE_PATH

app = Flask(__name__)

ex = Database(DATABASE_PATH)
NAMES = ['air_hudration_1', 'air_hudration_2', 'air_hudration_3', 'air_hudration_4', 'soil_hudration_1',
         'soil_hudration_2', 'soil_hudration_3', 'soil_hudration_4', 'soil_hudration_5', 'soil_hudration_6',
         'air_temperature_1', 'air_temperature_2',
         'air_temperature_3', 'air_temperature_4', 'greengouse_condition', 'door_condition', 'watering_garden_1',
         'watering_garden_2', 'watering_garden_3', 'watering_garden_4', 'watering_garden_5', 'watering_garden_6',
         'all_watering_garden']
NAMES_RU = ['Влажность воздуха на датчике 1', 'Влажность воздуха на датчике 2', 'Влажность воздуха на датчике 3',
            'Влажность воздуха на датчике 4',
            'Влажность почвы на датчике 1', 'Влажность почвы на датчике 2', 'Влажность почвы на датчике 3',
            'Влажность почвы на датчике 4', 'Влажность почвы на датчике 5',
            'Влажность почвы на датчике 6',
            'Температура воздуха на датчике 1', 'Температура воздуха на датчике 2', 'Температура воздуха на датчике 3',
            'Температура воздуха на датчике 4',
            'Экстренный режим', 'Состояние форточек',
            'Полив грядки номер 1', 'Полив грядки номер 2', 'Полив грядки номер 3', 'Полив грядки номер 4',
            'Полив грядки номер 5', 'Полив грядки номер 6', 'Система увлажнения воздуха']
flag = True
flag_2 = True
flag_3 = True
extra_mode = False
data = [False]

limit = open('limit.txt', 'r')
d = [[int(j) for j in i.split()] for i in limit.readlines()]
min_temp = d[0][0]
max_temp = d[0][1]
min_soil_hud = d[1][0]
max_soil_hud = d[1][1]
min_air_hud = d[2][0]
max_air_hud = d[2][1]
limit.close()

def change():
    d = ex.get_data_last()
    for i in range(16, 22):
        d[i] = 0
    ex.send_data(d, time.strftime('%x %X', time.localtime()))


def middle(data):
    return sum(data) / len(data)


def change_flag():
    global flag, flag_2, flag_3, extra_mode, min_temp, max_temp, min_soil_hud, max_soil_hud, min_air_hud, max_air_hud
    limit = open('limit.txt', 'r')
    d = [[int(j) for j in i.split()] for i in limit.readlines()]
    min_temp = d[0][0]
    max_temp = d[0][1]
    min_soil_hud = d[1][0]
    max_soil_hud = d[1][1]
    min_air_hud = d[2][0]
    max_air_hud = d[2][1]
    limit.close()
    if (not (middle(ex.get_data_last()[4:10]) > max_soil_hud) and not (middle(ex.get_data_last()[4:10]) <
                                                                       min_soil_hud)) or extra_mode:
        flag_2 = True
    else:
        flag_2 = False
        change()
    if (not (middle(ex.get_data_last()[10:14]) > max_temp) and not (middle(ex.get_data_last()[10:14]) <
                                                                    min_temp)) or extra_mode:
        flag = True
    else:
        flag = False
        d = ex.get_data_last()
        d[15] = 0
        ex.send_data(d, time.strftime('%x %X', time.localtime()))
    if (not (middle(ex.get_data_last()[:5]) > max_air_hud) and not (middle(ex.get_data_last()[:5]) <
                                                                    min_air_hud)) or extra_mode:
        flag_3 = True
    else:
        flag_3 = False
        d = ex.get_data_last()
        d[22] = 0
        ex.send_data(d, time.strftime('%x %X', time.localtime()))
    print(flag, flag_2, flag_3)


@app.route("/1", methods=["POST"])
def all():
    global flag, flag_2, flag_3, extra_mode
    sl1 = ex.get_data()
    return render_template('v1.html', key=list(sl1.keys())[-1], menu=sl1[list(sl1.keys())[-1]],
                           names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)


@app.route("/")
def index():
    global flag, flag_2
    change_flag()
    sl1 = ex.get_data()
    return render_template('v1.html', key=list(sl1.keys())[-1], menu=sl1[list(sl1.keys())[-1]],
                           names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)


@app.route("/1", methods=["POST"])
def index_2():
    global flag, flag_2
    change_flag()
    sl1 = ex.get_data()
    return render_template('v1.html', key=list(sl1.keys())[-1], menu=sl1[list(sl1.keys())[-1]],
                           names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)


@app.route('/door', methods=['POST'])
def doit():
    global flag, flag_2, flag_3, extra_mode
    change_flag()
    if flag:
        state = ex.get_data_last()[15]
        door_drive_request = "https://dt.miet.ru/ppo_it/api/fork_drive"
        patch = {
            "state": (state + 1) % 2
        }
        response = requests.patch(door_drive_request, params=patch)
        d = ex.get_data_last()
        d[15] = (state + 1) % 2
        print(d)
        ex.send_data(d, time.strftime('%x %X', time.localtime()))
        sl1 = ex.get_data()
        return render_template('v1.html', key=list(sl1.keys())[-1],
                               menu=sl1[list(sl1.keys())[-1]],
                               names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)
    else:
        sl1 = ex.get_data()
        return render_template('v1.html', key=list(sl1.keys())[-1],
                               menu=sl1[list(sl1.keys())[-1]],
                               names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)


@app.route('/watering_garden_<index>', methods=['POST'])
def doit_2(index):
    global flag, flag_2, flag_3, extra_mode
    change_flag()
    if flag_2:
        state = ex.get_data_last()[15 + int(index)]
        door_drive_request = "https://dt.miet.ru/ppo_it/api/watering"
        patch = {
            "id": index,
            "state": (state + 1) % 2
        }
        response = requests.patch(door_drive_request, params=patch)
        d = ex.get_data_last()
        d[15 + int(index)] = (state + 1) % 2
        print(d)
        print(1)
        ex.send_data(d, time.strftime('%x %X', time.localtime()))
        sl1 = ex.get_data()
        return render_template('v1.html', key=list(sl1.keys())[-1],
                               menu=sl1[list(sl1.keys())[-1]],
                               names=NAMES_RU, response=response, flag=flag, flag_2=flag_2, flag_3=flag_3)
    else:
        change()
        sl1 = ex.get_data()
        return render_template('v1.html', key=list(sl1.keys())[-1],
                               menu=sl1[list(sl1.keys())[-1]],
                               names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)


@app.route('/watering_garden_all', methods=['POST'])
def doit_3():
    global flag, flag_2, flag_3, extra_mode
    change_flag()
    if flag_3:
        state = ex.get_data_last()[22]
        door_drive_request = "https://dt.miet.ru/ppo_it/api/total_hum"
        patch = {
            "state": (state + 1) % 2
        }
        response = requests.patch(door_drive_request, params=patch)
        d = ex.get_data_last()
        if d[22] == 0:
            d[22] = 1
        else:
            d[22] = 0
        ex.send_data(d, time.strftime('%x %X', time.localtime()))
        sl1 = ex.get_data()
        return render_template('v1.html', key=list(sl1.keys())[-1],
                               menu=sl1[list(sl1.keys())[-1]],
                               names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)
    else:
        change()
        sl1 = ex.get_data()
        return render_template('v1.html', key=list(sl1.keys())[-1],
                               menu=sl1[list(sl1.keys())[-1]],
                               names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)



@app.route('/extra_mode', methods=['POST'])
def doit_4():
    global flag, flag_2, flag_3, extra_mode
    d = ex.get_data_last()
    if d[14] == 1:
        d[14] = 0
        extra_mode = False
    else:
        d[14] = 1
        extra_mode = True
        flag, flag_2, flag_3 = True, True, True
    ex.send_data(d, time.strftime('%x %X', time.localtime()))
    print(ex.get_data_last(), extra_mode)
    change_flag()
    sl1 = ex.get_data()
    return render_template('v1.html', key=list(sl1.keys())[-1], menu=sl1[list(sl1.keys())[-1]],
                           names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)


@app.route('/print')
def statistika():
    return render_template('img.html')


@app.route('/set')
def settings():
    limit = open('limit.txt', 'r')
    d = [[int(j) for j in i.split()] for i in limit.readlines()]
    min_temp = d[0][0]
    max_temp = d[0][1]
    min_soil_hud = d[1][0]
    max_soil_hud = d[1][1]
    min_air_hud = d[2][0]
    max_air_hud = d[2][1]
    limit.close()
    return render_template('set.html', text='', a=min_temp, b=max_temp, c=min_soil_hud, d=max_soil_hud, e=min_air_hud,
                           f=max_air_hud)


@app.route("/send", methods=["POST"])
def file_write():
    if request.method == 'POST':
        min_temp = request.form.get('min_temp')
        max_temp = request.form.get('max_temp')
        min_soil_hud = request.form.get('min_soil_hud')
        max_soil_hud = request.form.get('max_soil_hud')
        min_air_hud = request.form.get('min_air_hud')
        max_air_hud = request.form.get('max_air_hud')
        limit = open('limit.txt', 'r+')
        try:
            limit.write(f'{int(min_temp)} {int(max_temp)} \n {int(min_soil_hud)} {int(max_soil_hud)} \n {int(min_air_hud)}'
                        f' {int(max_air_hud)}')
        except ValueError:
            d = [[int(j) for j in i.split()] for i in limit.readlines()]
            min_temp = d[0][0]
            max_temp = d[0][1]
            min_soil_hud = d[1][0]
            max_soil_hud = d[1][1]
            min_air_hud = d[2][0]
            max_air_hud = d[2][1]
            limit.close()
            return render_template('set.html', text='Ошибка ввода данных', a=min_temp, b=max_temp, c=min_soil_hud,
                                   d=max_soil_hud, e=min_air_hud, f=max_air_hud)
        limit.close()
        sl1 = ex.get_data()
    change_flag()
    return render_template('v1.html', key=list(sl1.keys())[-1], menu=sl1[list(sl1.keys())[-1]],
                           names=NAMES_RU, flag=flag, flag_2=flag_2, flag_3=flag_3)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
