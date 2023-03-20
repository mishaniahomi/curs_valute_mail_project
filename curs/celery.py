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
    sender.add_periodic_task(60*60*24, test.s('hello'), name='add every 10')


@app.task
def test(arg):
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
    date = begin
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
        cur.datetime = date
        cur.value = float(i.Value.contents[0].replace(',', '.'))
        cur.save()
