import requests
import datetime
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from celery import shared_task

from celery import shared_task

@shared_task
def allsend(args):
    from main.models import Contact
    users = Contact.objects.all()
    for user in users:
        send.delay(user.email, user.name)



@shared_task
def get_curs_now():
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
    responce = requests.post(url)
    if responce.status_code != 200:
        raise ValueError(f"Request add_user failed {responce.status_code}")
    resp_xml_content = responce.content
    soup = BeautifulSoup(resp_xml_content, 'lxml-xml')
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



@shared_task
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