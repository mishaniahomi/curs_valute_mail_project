"""
Файл настроек Celery
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
from __future__ import absolute_import
import os
from celery import Celery
import requests
import datetime
from bs4 import BeautifulSoup
from celery.schedules import crontab
from django.core.mail import send_mail
# этот код скопирован с manage.py
# он установит модуль настроек по умолчанию Django для приложения 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'send_email.settings')
import time
# здесь вы меняете имя
app = Celery("send_email")

# Для получения настроек Django, связываем префикс "CELERY" с настройкой celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# загрузка tasks.py в приложение django
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=9, minute=30, day_of_week=0), test.s('Обновление данных воскресенье'), name='0')
    sender.add_periodic_task(crontab(hour=9, minute=30, day_of_week=1), test.s('Обновление данных воскресенье'), name='1')
    sender.add_periodic_task(crontab(hour=9, minute=30, day_of_week=2), test.s('Обновление данных воскресенье'), name='2')
    sender.add_periodic_task(crontab(hour=9, minute=30, day_of_week=3), test.s('Обновление данных воскресенье'), name='3')
    sender.add_periodic_task(crontab(hour=9, minute=30, day_of_week=4), test.s('Обновление данных воскресенье'), name='4')
    sender.add_periodic_task(crontab(hour=9, minute=30, day_of_week=5), test.s('Обновление данных воскресенье'), name='5')
    sender.add_periodic_task(crontab(hour=9, minute=30, day_of_week=6), test.s('Обновление данных воскресенье'), name='6')

    sender.add_periodic_task(crontab(hour=12, minute=4, day_of_week=0), allsend.s('Рассылка воскресенье'), name='Рассылка воскресенье')
    sender.add_periodic_task(crontab(hour=12, minute=4, day_of_week=1), allsend.s('Рассылка понедельник'), name='Рассылка понедельник')
    sender.add_periodic_task(crontab(hour=12, minute=4, day_of_week=2), allsend.s('Рассылка вторник'), name='Рассылка вторник')
    sender.add_periodic_task(crontab(hour=12, minute=4, day_of_week=3), allsend.s('Рассылка среда'), name='Рассылка среда')
    sender.add_periodic_task(crontab(hour=12, minute=4, day_of_week=4), allsend.s('Рассылка четверг'), name='Рассылка четверг')
    sender.add_periodic_task(crontab(hour=12, minute=4, day_of_week=5), allsend.s('Рассылка пятница'), name='Рассылка пятница')
    sender.add_periodic_task(crontab(hour=12, minute=4, day_of_week=6), allsend.s('Рассылка суббота'), name='Рассылка суббота')


@app.task
def allsend(args):
    from main.models import Contact
    users = Contact.objects.all()
    for user in users:
        send.delay(user.email, user.name)



@app.task
def test(args):
    from .models import Curs, Valute
    begin = datetime.datetime.now()
    if begin.day > 9:
        d = begin.day
    else:
        d = f'0{begin.day}'
    if begin.month > 9:
        m = begin.month
    else:
        m = f'0{begin.month}'
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={d}/{m}/{begin.year}'
    # url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=19/03/2023'
    responce = requests.post(url)
    if responce.status_code != 200:
        raise ValueError(f"Request add_user failed {responce.status_code}")
    resp_xml_content = responce.content
    soup = BeautifulSoup(resp_xml_content, 'lxml-xml')
    print(soup)
    for i in soup.ValCurs:
        try:
            val = Valute.objects.get(unique_id=i['ID'])
        except:
            val = Valute()
            val.unique_id = i['ID']
            val.num_code = int(i.NumCode.contents[0])
            val.char_code = i.CharCode.contents[0]
            val.nominal = int(i.Nominal.contents[0])
            val.name = i.Name.contents[0]
            val.save()
        cur = Curs()
        cur.valute_id = val
        cur.datetime = begin
        cur.value = float(i.Value.contents[0].replace(',', '.'))
        cur.save()
    return soup


@app.task
def send(user_email, name):
    from .models import Curs
    data = Curs.objects.filter(datetime__gte=datetime.datetime.now()-datetime.timedelta(1)).order_by('datetime')
    str_list = []
    for i in data:
        str_list.append("{} {}\n".format(i.valute_id, i.value))

    return send_mail(
        'Здравствуйте, {} Вот курсы валют:'.format(name),
        '\n '.join(str_list),
        'P.S. MishaniaHomi',
        [user_email],
        fail_silently=False
    )