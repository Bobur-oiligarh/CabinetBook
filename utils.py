from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML
import smtplib
import ssl


def send_email(client_email: str, theme: str, text: str):
    addr_from = "uboiligarh@gmail.com"
    addr_to = client_email
    password = 'bobur19901111'

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = theme

    body = text
    msg.attach(MIMEText(body, 'plain'))

    # port = 465
    # 
    # context = ssl.create_default_context()

    server = smtplib.SMTP('smtp.gmail.com', 587)           # Создаем объект SMTP
    server.set_debuglevel(True)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()                                   # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)                   # Получаем доступ
    server.send_message(msg)                            # Отправляем сообщение
    server.quit()

   
        

        
        
def hour2minutes(hours):
    start, end = hours[0], hours[1]
    starthour, startmins = start.split(":")
    endhour, endmins = end.split(":")
    startminute = int(starthour)*60+int(startmins)
    endminute = int(endhour)*60+int(endmins)

    return [startminute, endminute]