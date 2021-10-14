from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML
import smtplib
import ssl


def send_email(client_email: str, theme: str, text: str):
    address_from = "uboiligar@gmail.com"
    address_to = client_email

    msg = MIMEMultipart()
    msg['From'] = address_from
    msg['To'] = address_to
    msg['Subject'] = theme

    body = text
    msg.attach(MIMEText(body, 'plain'))

    port = 465
    password = 'bobur19901111'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("uboiligarh@gmail.com", password)
        server.set_debuglevel(True)  # Включаем режим отладки
        server.send_message(msg)  # Отправляем сообщение


def hour2minutes(hours):
    start, end = hours[0], hours[1]
    starthour, startmins = start.split(":")
    endhour, endmins = end.split(":")
    startminute = int(starthour)*60+int(startmins)
    endminute = int(endhour)*60+int(endmins)

    return [startminute, endminute]