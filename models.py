import sqlite3


class Database:
    """ Создадим класс для связи с БД, записи, чтения данных из базы данных """
    def __init__(self, path_to_db='cabinet_book_db.db'):        # Передадим классу параметром путь к БД. При отсутствии он создаст новый
        self.path_to_db = path_to_db

    @property
    def connection(self):
        """Функция создания соединения с БД sqlite3"""
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None,
                fetchone=False, fetchall=False, commit=False):
        """ Функция для выполнения запросов в sqlite """
        connection = self.connection
        cursor = connection.cursor()
        data = None

        if parameters is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def cabinettable(self):
        """ Функция для создания таблицы Cabinet в БД """
        sql = """
            CREATE TABLE "Cabinet" (
                   "id"  INTEGER PRIMARY KEY AUTOINCREMENT
            ); 
        """
        self.execute(sql, commit=True)

    def clienttable(self):
        """ Функция для создания таблицы Client в БД"""
        sql = """
            CREATE TABLE "Client" (
                "id"  INTEGER PRIMARY KEY AUTOINCREMENT,
                "name"  TEXT,
                "email"  TEXT,
                "phone"  TEXT
            );
        """
        self.execute(sql, commit=True)

    def booktable(self):
        """ Функция для создания таблицы Book в БД"""
        sql = """
            CREATE TABLE "Book" (
                "id"  INTEGER,
                "cabinet"  INTEGER,
                "client"  INTEGER,
                "booked_date"  TEXT,
                "booked_time"  TEXT,
                "how_long"  TEXT,
                "book_end_date"  TEXT,
                "book_end_time"  TEXT,
                FOREIGN KEY("client") REFERENCES "Client"("id"),
                FOREIGN KEY("cabinet") REFERENCES "Cabinet"("id"),
                PRIMARY KEY("id")
            );
        """
        self.execute(sql, commit=True)

db = Database()
db.cabinettable()      # Вызовим методы класса и создадим таблицы
db.clienttable()
db.booktable()

