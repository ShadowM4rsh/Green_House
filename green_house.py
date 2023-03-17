import requests
import schedule
import time
from database_pr import Database
from config.settings import DATABASE_PATH
import graphics


ex = Database(DATABASE_PATH)
#Библиотеки + дб + рисовка графиков

class GreenHouse:
    def __init__(self):
        self.temp = [0, 0, 0, 0] #Темпераура + влажность, 4 датчика (кортеж)
        self.gr_hyd = [0, 0, 0, 0, 0, 0] #Влажность почвы, 6 датчиков
        self.drive = 0 #Состояние привода форточек, 1 - работает, 0 - не работает
        self.watering = [0, 0, 0, 0, 0, 0] #Состояние поливалок,6 шт., 1 - работает, 0 - не работает
        self.hyd = 0 #Состояние привода единой системы увлажнения, 1 - работает, 0 - не работает
        self.average_t = float() #Средняя температура
        self.average_h = float() #Средняя влажность
        self.average_grh = float() #Средняя влажность почвы
        self.temp_limit = (25, 34) #Возможные диапазоны температуры
        self.hyd_limit = (40, 80) #Возможные диапазоны влажности
        self.gr_hyd_limit = (40, 80) #Возможные диапазоны влажности почвы
        self.emergency_mode_enabled = 0 #Состояние экстренного режима управления теплицей, 1 - работает, 0 - не работает

    def doors_drive(self, state): #Отправка состояния о включении или выключении привода форточек
        door_drive_request = "https://dt.miet.ru/ppo_it/api/fork_drive"
        patch = {
            "state": state
        }
        response = requests.patch(door_drive_request, params=patch)
        if response:
            self.drive = state
            return self.drive
        else:
            print("Ошибка выполнения запроса:")
            print(door_drive_request)
            return "Http статус:", response.status_code, "(", response.reason, ")"


    def watering_switch(self, num, state): #Отправка состояния о включении или выключении поливалки на грядке
        watering_request = "https://dt.miet.ru/ppo_it/api/watering"
        patch = {
            "id": num,
            "state": state
        }
        response = requests.patch(watering_request, params=patch)
        if response:
            self.watering[num - 1] = state
            return "done"
        else:
            print("Ошибка выполнения запроса:")
            print(watering_request)
            return "Http статус:", response.status_code, "(", response.reason, ")"


    def hyd_drive(self, state): #Отправка состояния о включении или выключении единой системы увлажнения воздуха
        hyd_request = "https://dt.miet.ru/ppo_it/api/total_hum"
        patch = {
            "state": state
        }
        response = requests.patch(hyd_request, params=patch)
        if response:
            self.hyd = state
            return "done"
        else:
            print("Ошибка выполнения запроса:")
            print(hyd_request)
            return "Http статус:", response.status_code, "(", response.reason, ")"

    def get_temp_hyd_value(self, num): #Получение температуры и влажности с определённого датчика
        temp_hyd_request = f"https://dt.miet.ru/ppo_it/api/temp_hum/{num}"
        response = requests.get(temp_hyd_request)
        if response:
            json_response = response.json()
            self.temp[json_response["id"] - 1] = (json_response["temperature"], json_response["humidity"])
            return "done"
        else:
            print("Ошибка выполнения запроса:")
            print(temp_hyd_request)
            return "Http статус:", response.status_code, "(", response.reason, ")"

    def get_ground_hyd_value(self, num): #Получение влажности почвы с определённого датчика
        gr_hyd_request = f"https://dt.miet.ru/ppo_it/api/hum/{num}"
        response = requests.get(gr_hyd_request)
        if response:
            json_response = response.json()
            self.gr_hyd[json_response["id"] - 1] = json_response["humidity"]
            return "done"
        else:
            print("Ошибка выполнения запроса:")
            print(gr_hyd_request)
            return "Http статус:", response.status_code, "(", response.reason, ")"

    def get_all_th_values(self): #Получение температуры и влажности со всех датчиков
        for i in range(1, 5):
            self.get_temp_hyd_value(i)

    def get_all_gr_values(self): #Получение влажности почвы со всех датчиков
        for i in range(1, 7):
            self.get_ground_hyd_value(i)

    def update_all(self): #Обновление всех данных
        self.get_all_th_values()
        self.get_all_gr_values()

    def send_all(self): #Отправка всех данных в дб
        values = list()
        for elem in self.temp:
            values.append(elem[1])
        for elem in self.gr_hyd:
            values.append(elem)
        for elem in self.temp:
            values.append(elem[0])
        d = ex.get_data_last()[14:]
        values += d
        ex.send_data(values, time.strftime('%x %X', time.localtime()))

    def average_temh(self): #Подсчёт средней температуры и влажности
        for elem in self.temp:
            self.average_h += elem[1]
            self.average_t += elem[0]
        self.average_h /= 4
        self.average_t /= 4
        return (self.average_t, self.average_h)

    def average_grhyd(self): #Подсчёт средней влажности почвы
        for elem in self.gr_hyd:
            self.average_grh += elem
        self.average_grh /= 6
        return self.average_grh

    def give_values_temp(self): #Рисовка графика температуры всех датчиков
        minute = time.strftime('%x %X', time.localtime()).split()[1][:5]
        graphics.plot_graph_temperatyre(minute, [x[0] for x in self.temp])

    def give_values_hyd(self): #Рисовка графика влажности всех датчиков
        minute = time.strftime('%x %X', time.localtime()).split()[1][:5]
        graphics.plot_graph_airhyd(minute, [x[1] for x in self.temp])

    def give_values_soilhyd(self): #Рисовка графика влажности почвы всех датчиков
        minute = time.strftime('%x %X', time.localtime()).split()[1][:5]
        graphics.plot_graph_soilhyd(minute, [x for x in self.gr_hyd])

    def give_average_values_temp(self): #Рисовка графика средней температуры
        minute = time.strftime('%x %X', time.localtime()).split()[1][:5]
        graphics.plot_graph_average_temp(minute, self.average_t)

    def give_average_values_hyd(self): #Рисовка графика средней влажности
        minute = time.strftime('%x %X', time.localtime()).split()[1][:5]
        graphics.plot_graph_average_hyd(minute, self.average_h)

    def give_average_values_soilhyd(self): #Рисовка графика средней влажности почвы
        minute = time.strftime('%x %X', time.localtime()).split()[1][:5]
        graphics.plot_graph_average_soilhyd(minute, self.average_grh)

    def mid_stats(self):
        sl = ex.get_data()
        key = list(sl.keys())
        minute = [round(sum(sl[key[-1]][:4]) / 4, 1), round(sum(sl[key[-1]][4:10]) / 6, 1),
                  round(sum(sl[key[-1]][10:14]) / 4, 1)]
        if len(key) >= 5:
            fi = [round(sum([sum(sl[key[i]][:4]) for i in range((len(key) - 5), len(key))]) / 20, 1),
                  round(sum([sum(sl[key[i]][4:10]) for i in range((len(key) - 5), len(key))]) / 30, 1),
                  round(sum([sum(sl[key[i]][10:14]) for i in range((len(key) - 5), len(key))]) / 30, 1)]
            if len(key) >= 10:
                te = [round(sum([sum(sl[key[i]][:4]) for i in range((len(key) - 10), len(key))]) / 40, 1),
                      round(sum([sum(sl[key[i]][4:10]) for i in range((len(key) - 10), len(key))]) / 60, 1),
                      round(sum([sum(sl[key[i]][10:14]) for i in range((len(key) - 10), len(key))]) / 40, 1)]
                if len(key) >= 30:
                    hf = [round(sum([sum(sl[key[i]][:4]) for i in range((len(key) - 30), len(key))]) / 120, 1),
                          round(sum([sum(sl[key[i]][4:10]) for i in range((len(key) - 30), len(key))]) / 180, 1),
                          round(sum([sum(sl[key[i]][10:14]) for i in range((len(key) - 30), len(key))]) / 120, 1)]
                    if len(key) >= 60:
                        ho = [round(sum([sum(sl[key[i]][:4]) for i in range((len(key) - 60), len(key))]) / 240, 1),
                              round(sum([sum(sl[key[i]][4:10]) for i in range((len(key) - 60), len(key))]) / 360, 1),
                              round(sum([sum(sl[key[i]][10:14]) for i in range((len(key) - 60), len(key))]) / 240, 1)]
                        if len(key) >= 720:
                            tw = [
                                round(sum([sum(sl[key[i]][:4]) for i in range((len(key) - 720), len(key))]) / 2880, 1),
                                round(sum([sum(sl[key[i]][4:10]) for i in range((len(key) - 720), len(key))]) / 4320,
                                      1),
                                round(sum([sum(sl[key[i]][10:14]) for i in range((len(key) - 720), len(key))]) / 2880,
                                      1)]
                        else:
                            tw = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                    else:
                        ho = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                        tw = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                else:
                    hf = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                    ho = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                    tw = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
            else:
                te = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                hf = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                ho = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
                tw = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
        else:
            fi = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
            te = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
            hf = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
            ho = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
            tw = ["Данные ещё не поступили", "Данные ещё не поступили", "Данные ещё не поступили"]
        al = [round(sum([sum(sl[key[i]][:4]) for i in range(len(key))]) / (len(key) * 4), 1),
              round(sum([sum(sl[key[i]][4:10]) for i in range(len(key))]) / (len(key) * 6), 1),
              round(sum([sum(sl[key[i]][10:14]) for i in range(len(key))]) / (len(key) * 4), 1)]
        return graphics.draw_table([minute, fi, te, hf, ho, tw, al])

    def clear(self):
        graphics.clear()

    def all_graphics(self): #Рисовка всех графиков (РИСУЕТ CEXRF!!!)
        self.clear()
        self.give_values_temp()
        self.give_values_hyd()
        self.give_values_soilhyd()
        self.give_average_values_temp()
        self.give_average_values_hyd()
        self.give_average_values_soilhyd()
        self.mid_stats()


tep = GreenHouse()
tep.doors_drive(0)
for i in range(1, 7):
    tep.watering_switch(i, 0)
tep.hyd_drive(0)
tep.update_all()
tep.send_all()
tep.average_temh()
tep.average_grhyd()
tep.all_graphics()
tep.mid_stats()
schedule.every(1).minute.do(tep.update_all)
schedule.every(1).minute.do(tep.send_all)
schedule.every(1).minute.do(tep.average_temh)
schedule.every(1).minute.do(tep.average_grhyd)
schedule.every(1).minute.do(tep.all_graphics)
while True:
    schedule.run_pending()
    time.sleep(1)
