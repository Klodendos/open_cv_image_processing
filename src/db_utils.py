import sqlite3


class DBUtils:
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBUtils, cls).__new__(cls)
        return cls._instance

    def connect(self):
        self.connection = sqlite3.connect('../config/image_processing.db')
        self.cursor = self.connection.cursor()
        self.__create_results_table()

    def disconnect(self):
        self.connection.commit()
        self.connection.close()

    def __create_results_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS processing_results (
        id integer PRIMARY KEY,
        center_x integer,
        center_y integer,
        dispersion float,
        deviation float
        )
        ''')

    def update_results_table(self, results):
        self.cursor.execute('''
        INSERT INTO processing_results (center_x, center_y, dispersion, deviation) 
        VALUES (?, ?, ?, ?)
        ''',
                            (results['center_position'][0],
                             results['center_position'][1],
                             float(results['dispersion']),
                             float(results['deviation']))
                            )
        self.connection.commit()
