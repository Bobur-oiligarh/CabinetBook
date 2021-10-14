import datetime
import time
from models import Database
from utils import hour2minutes, send_email

db = Database()
cabinets = db.get_cabinets()  # Объявляем все кабинеты в переменную cabinets. Возвращает список из tuple элементов
cabinets = [str(i[0]) for i in cabinets]  # Для удобства манипуляции меняем список кабинетов в tuple на список str
print(f""" Добро пожаловать! Какой кабинет хотите забронировать?  
     На данный момент у нас работают следующие кабинеты:
    {", ".join(cabinets)}
    """)
cab_for_check = input("Введите пожалуйста номер кабинета:")
date_for_check = input("""В какой день и время вы хотите бронировать? 
                       Введите в формате: YYYY-MM-DD HH:mm """)
orders = db.check(id=int(cab_for_check),
                  date=date_for_check.split()[0])  # Получаем список tuple бронированных времен
lst = list(map(lambda x: f"{x[0]} - {x[1]}", orders))  # Переводим в список
newline = '\n'
results = []
if len(orders) > 0:  # Если есть броны кабинета, то выводим их
    print(f"Здесь все броны на эту дату:{newline * 2}{newline.join(lst)}{newline}")
else:
    print('На эту дату кабинет не забронирован! Можете смело бронировать!')

orders_in_minutes = list(map(hour2minutes, orders))  # Получим лист времен заказов в минутах
asked_time = date_for_check.split()[1]  # Вырезаем только время из введенного дата + время
hour, minute = asked_time.split(':')  # Полученный результат присваиваем переменным
asked_time_in_minutes = (int(hour) * 60) + int(minute)  # Переведем запрашиваемое время тоже в минуты
count = 0  # Счетчик
booked_index = 0

for i in orders_in_minutes:  # Проверяем кабинет на свободность
    if i[0] <= asked_time_in_minutes < i[1]:  # Если запрашиваемое время попало в интервал заброна.
        results.append(True)  # Добавляем True в лист results
        booked_index = count  # Ведем учет пересечения запрашиваемого и заброн времени
    else:
        results.append(False)
    count += 1
print(results, orders_in_minutes, orders)

if sum(results) > 0:  # Если есть хотя бы один True
    print("На это время кабинет забронирован, введите другое время! \n"
          "Программа прекратит свою работу! \n")

    booked = db.get_booked(startdate=date_for_check.split()[0],  # Получим заказ, где наш брон был неуспешным
                           starttime=orders[booked_index][0],
                           enddate=date_for_check.split()[0],
                           endtime=orders[booked_index][1], )
    print(booked)
    client_id = booked[-1]  # Получаем ID клиента, который забронировал до нас для смс
    client = db.get_client(id=client_id)
    print(client)

    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)
    exit()
how_long = input("""На сколько хотите бронировать? \n""")

timedelta = datetime.timedelta(hours=float(how_long))

if len(date_for_check.split()[1]) > 4:    # Если введен правильный формат времени
    pass
else:       # Если введено неправильный формат времени, поправим это
    dt, tt = date_for_check.split()
    ttt = '0' + tt
    date_for_check = " ".join([dt, ttt])
checked_date = datetime.datetime.fromisoformat(date_for_check)
expected_end_time = checked_date + timedelta    # Конец времени ожидаемого заказа дата + время
strexpected = expected_end_time.time().strftime("%H:%M")    # Захватываем время только
asked_end_time = strexpected    # Конец времени ожидаемого заказа
h, m = asked_end_time.split(':')
asked_end_min = (int(h) * 60) + int(m)    # В минутах

results2 = []     # Лист True, False. Где False кабинет свободен полностью
count2 = 0
booked_index2 = 0
for i in orders_in_minutes:
    if asked_time_in_minutes < i[0] < asked_end_min:    # Проверяем условие когда время заказа заходит в забронирован
        results2.append(True)
        booked_index2 = count2  # Индексируем каждое такое пересечение ожидаемого и забронированого
    else:
        results2.append(False)  # В это время кабинет свободен
    count2 += 1
print(results2, orders_in_minutes, orders)

if sum(results2) > 0:   # Если есть хотя бы одно такое пересечение времен
    booked = db.booked(startdate=date_for_check.split()[0],
                       starttime=orders[booked_index2][0],
                       enddate=date_for_check.split()[0],
                       endtime=orders[booked_index2][1], )
    print(
        f"К сожалению мы не можем забронировать кабинет на такой период, так как он уже занят с ???\n\n"
        f"Программа завершит работу! ")
    print(booked)
    client_id = booked[-1]
    client = db.get_client(id=client_id)
    print(client)
    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)
    exit()

if sum(results) == 0 and sum(results2) == 0:  # Если в обеих листах все False, то есть кабинет свободен весь день
    yes_or_not = input("""В запрашиваемый день кабинет свободень. Будете бронировать? Д(a)/Н(ет)\n""")
    if yes_or_not.lower() == 'д':
        book_start_day = datetime.datetime.fromisoformat(date_for_check).date()
        book_start_time = datetime.datetime.fromisoformat(date_for_check).time()
        name = input("""Пожалуйста введите имя клиента: """)
        email = input("""Теперь электронный адресс клиента пожалуйста: """)
        phone = input("""Введите пожалуйста телефонный номер клиента: """)
        db.clientadd(name=name,     # Записываем нового клиента в БД
                     email=email,
                     phone=phone)
        last_client = db.get_last_client()[0]    # Получаем только зарегистрированного клиента
        db.book(cabinet=int(cab_for_check),     # Регистрируем данные о броне кабинета в БД
                booked_date=date_for_check.split()[0],
                booked_time=date_for_check.split()[1],
                how_long=float(how_long),
                book_end_date=expected_end_time.date().strftime('%Y-%m-%d'),
                book_end_time=strexpected,
                client=last_client
                )
        print('\n', 'Кабинет успешнозабронирован!')
        send_email(client_email=email, theme="Забронирован кабинет",
                   text=f"""Заказанный Вами кабинет - {cab_for_check} с {date_for_check} 
                   по {expected_end_time.date().strftime('%Y-%m-%d')} {strexpected}
                   учпешно забронирован!""")
    else:
        print("Досвидание! ")