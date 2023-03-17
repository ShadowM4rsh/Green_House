import sqlite3

CREATE_DATABASE_QUERY = f"""
CREATE TABLE sensors (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT
                                 UNIQUE
                                 NOT NULL,
    air_humidity_1      REAL    DEFAULT (0),
    air_humidity_2      REAL    DEFAULT (0),
    air_humidity_3      REAL    DEFAULT (0),
    air_humidity_4      REAL    DEFAULT (0),
    soil_humidity_1     REAL    DEFAULT (0),
    soil_humidity_2     REAL    DEFAULT (0),
    soil_humidity_3     REAL    DEFAULT (0),
    soil_humidity_4     REAL    DEFAULT (0),
    soil_humidity_5     REAL    DEFAULT (0),
    soil_humidity_6     REAL    DEFAULT (0),
    air_temperature_1    REAL    DEFAULT (0),
    air_temperature_2    REAL    DEFAULT (0),
    air_temperature_3    REAL    DEFAULT (0),
    air_temperature_4    REAL    DEFAULT (0),
    greengouse_condition INTEGER DEFAULT (0),
    door_condition       INTEGER DEFAULT (0),
    watering_garden_1    INTEGER DEFAULT (0),
    watering_garden_2    INTEGER DEFAULT (0),
    watering_garden_3    INTEGER DEFAULT (0),
    watering_garden_4    INTEGER DEFAULT (0),
    watering_garden_5    INTEGER DEFAULT (0),
    watering_garden_6    INTEGER DEFAULT (0),
    all_watering_garden  INTEGER DEFAULT (0),
    time                 TEXT    DEFAULT [00:00:00]
);
"""

class Database:
    def __init__(self, name):
        self.db_name = name
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        try:
            self.result = cur.execute(CREATE_DATABASE_QUERY).fetchall()
            self.send_data([0] * 24, '00:00:00')
        except sqlite3.OperationalError:
            self.result = cur.execute("""SELECT * FROM  sensors""").fetchall()
        cur.close()
        con.close()

    def get_data(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        self.result = cur.execute("""SELECT * FROM  sensors""").fetchall()
        cur.close()
        con.close()
        sl = {}
        for i in self.result:
            sl[i[-1]] = list(i[1:-1])
        return sl

    def get_data_last(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        self.result = cur.execute("""SELECT * FROM  sensors""").fetchall()
        cur.close()
        con.close()
        sl = {}
        for i in self.result:
            sl[i[-1]] = list(i[1:-1])
        return sl[list(sl.keys())[-1]]

    def send_data(self, data, time):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(f"""INSERT INTO sensors(air_humidity_1, air_humidity_2, air_humidity_3, air_humidity_4,
                soil_humidity_1, soil_humidity_2, soil_humidity_3, soil_humidity_4, soil_humidity_5,
                soil_humidity_6, air_temperature_1, air_temperature_2, air_temperature_3, air_temperature_4,
                greengouse_condition, door_condition, watering_garden_1, watering_garden_2, watering_garden_3,
                watering_garden_4,  watering_garden_5, watering_garden_6, all_watering_garden, time)
                VALUES({data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]},
                {data[6]}, {data[7]}, {data[8]}, {data[9]}, {data[10]}, {data[11]}, {data[12]}, {data[13]}, {data[14]},
                {data[15]}, {data[16]}, {data[17]}, {data[18]}, {data[19]}, {data[20]}, {data[21]}, {data[22]},
                '{time}')""")
        con.commit()
        cur.close()

