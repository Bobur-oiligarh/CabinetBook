import datetime
import time
from models import Database
from utils import hour2minutes, send_email, send_sms

db = Database()
cabinets = db.get_cabinets()  # Объявляем все кабинеты в переменную cabinets. Возвращает список из tuple элементов
cabinets = [str(i[0]) for i in cabinets]  # Для удобства манипуляции меняем список кабинетов в tuple на список str
print(f""" Добро пожаловать! Какой кабинет хотите забронировать?  
     На данный момент у нас работают следующие кабинеты:
    {", ".join(cabinets)}
    """)
cab_for_check = input("Введите пожалуйста номер кабинета:")
email = input("""Введите электронный адресс для получения информации: """)
phone = input("""Введите валидный номер телефона, в виде +998901234567: """)
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

if sum(results) > 0:  # Если есть хотя бы один True
    print("На это время кабинет забронирован, введите другое время! \n"
          "Программа прекратит свою работу! \n")

    booked = db.get_booked(startdate=date_for_check.split()[0],  # Получим заказ, где наш брон был неуспешным
                           starttime=orders[booked_index][0],
                           enddate=date_for_check.split()[0],
                           endtime=orders[booked_index][1], )    
    client_id = booked[2]  # Получаем ID клиента, который забронировал до нас для смс
    client = db.get_client(id=client_id)
    client_name = client[1]
    booked_to = booked[-1]    
    time.sleep(2)
    for i in range(10, 0, -1):
        print(i)
        time.sleep(0.1)

    send_email(client_email=email, theme="Кабинет занят!", text=f"{cab_for_check} кабинет уже забронирован господином - {client_name},"
                    f" до {date_for_check.split()[0]} {booked_to}")    

    send_sms(client_phone=phone, text=f"{cab_for_check} кабинет уже забронирован господином - {client_name},"
                                      f" до {date_for_check.split()[0]} {booked_to}") 
    exit()

how_long = input("""Как долго хотите забронировать? \n""")

timedelta = datetime.timedelta(hours=float(how_long))

if len(date_for_check.split()[1]) > 4:    # Если введен правильный формат времени
    pass
else:       # Если введено неправильный формат времени, поправим это
    date, time = date_for_check.split()
    correct_time = '0' + time
    date_for_check = " ".join([date, correct_time])
    
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

if sum(results2) > 0:   # Если есть хотя бы одно такое пересечение времен
    booked = db.get_booked(startdate=date_for_check.split()[0],
                       starttime=orders[booked_index2][0],
                       enddate=date_for_check.split()[0],
                       endtime=orders[booked_index2][1], )
    client_id = booked[2]
    client = db.get_client(id=client_id)
    client_name = client[1]
    booked_to = booked[-1]
    
    print(
        f"К сожалению мы не можем забронировать кабинет на такой период, так как он уже занят с {booked[4]}\n\n"
        f"Введите другое время.Программа завершит работу! ")
  
    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)
    send_email(client_email=email, theme="Кабинет занят!", text=f"{cab_for_check} кабинет уже забронирован господином - {client_name},"
                                                                f" до {date_for_check.split()[0]} {booked_to}")    

    send_sms(client_phone=phone, text=f"{cab_for_check} кабинет уже забронирован господином - {client_name},"
                                      f" до {date_for_check.split()[0]} {booked_to}")
    exit()

if sum(results) == 0 and sum(results2) == 0:  # Если в обеих листах все False, то есть кабинет свободен 
    yes_or_not = input("""В запрашиваемый день кабинет свободень. Будете бронировать? Д(a)/Н(ет)\n""")
    if yes_or_not.lower() == 'д':
        book_start_day = datetime.datetime.fromisoformat(date_for_check).date()
        book_start_time = datetime.datetime.fromisoformat(date_for_check).time()
        name = input("""Пожалуйста введите имя клиента: """)        
        db.add_client(name=name,     # Записываем нового клиента в БД
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
        print('\n', 'Кабинет успешно забронирован!')
         
        send_email(client_email=email, theme="Кабинет забронирован!",
                   text=f"Вы успешно забронировали кабинет № {cab_for_check} с {date_for_check} по "
                        f"{expected_end_time.date().strftime('%Y-%m-%d')} {strexpected}")
        send_sms(client_phone=phone, text=f"Вы успешно забронировали кабинет № {cab_for_check} с {date_for_check} по "
                                          f"{expected_end_time.date().strftime('%Y-%m-%d')} {strexpected}"  )
    else:
        print("Досвидание! ")
        exit()




    