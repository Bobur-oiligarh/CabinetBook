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
        sql = """CREATE TABLE "Cabinet" (
                   "id"  INTEGER PRIMARY KEY AUTOINCREMENT
            ); 
        """
        self.execute(sql, commit=True)

    def clienttable(self):
        """ Функция для создания таблицы Client в БД"""
        sql = """CREATE TABLE "Client" (
                "id"  INTEGER PRIMARY KEY AUTOINCREMENT,
                "name"  TEXT,
                "email"  TEXT,
                "phone"  TEXT
            );
        """
        self.execute(sql, commit=True)

    def booktable(self):
        """ Функция для создания таблицы Book в БД"""
        sql = """CREATE TABLE "Book" (
                "id"  INTEGER PRIMARY KEY AUTOINCREMENT,
                "cabinet"  INTEGER,
                "client"  INTEGER,
                "booked_date"  TEXT,
                "booked_time"  TEXT,
                "how_long"  TEXT,
                "book_end_date"  TEXT,
                "book_end_time"  TEXT,
                FOREIGN KEY("client") REFERENCES "Client"("id"),
                FOREIGN KEY("cabinet") REFERENCES "Cabinet"("id")               
            );
        """
        self.execute(sql, commit=True)

    def add_cabinet(self, id):
        """ Функция для записи данных в БД"""
        sql = """INSERT INTO Cabinet(id) VALUES (?)"""
        param = (id,)
        self.execute(sql=sql, parameters=param, commit=True)

    def add_client(self, name: str, email: str = None, phone=str):
        """ Функция для записи данных клиента в БД"""
        sql = """INSERT INTO Client(name, email, phone) VALUES (?,?,?)"""
        parameters = (name, email, phone)
        self.execute(sql, parameters=parameters, commit=True, fetchall=True)

    def get_cabins(self):
        """ Функция для получения всех кабинетов"""
        return self.execute("""SELECT * FROM Cabinet""", fetchall=True)

    def get_client(self, id):
        """ Функция возвращает клиента с данным ID """
        sql = """SELECT * FROM Client WHERE id=(?)"""
        param = (id,)
        return self.execute(sql=sql, parameters=param, fetchone=True)

    def check(self, id, date):
        """ Функция возвращает список начальных и конечных времен бронирования, если они есть, для выбранного кабинета
         в выбранную дату"""
        sql = """SELECT booked_time,book_end_time FROM Book WHERE cabinet=(?) AND booked_date=(?)"""
        param = (id, date)
        return self.execute(sql=sql, parameters=param, fetchall=True)

    def book(self, cabinet, booked_date, booked_time, how_long, book_end_date, book_end_time, client):
        """Функция для записи в БД данных о текущем бронировании"""
        sql = """INSERT INTO Book(cabinet, booked_date, booked_time, how_long, book_end_date, book_end_time, client)
                    VALUES (?,?,?,?,?,?,?);
           """
        param = (cabinet, booked_date, booked_time, how_long, book_end_date, book_end_time, client)
        self.execute(sql=sql, parameters=param, commit=True)


db = Database()
# db.cabinettable()      # Вызовим методы класса и создадим таблицы
# db.clienttable()
# db.booktable()

for i in [1, 2, 3, 4, 5]:
    db.add_cabinet(id=i)






