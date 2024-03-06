from typing import Any
from django.core.management.base import BaseCommand

from curs.models import Curs, Valute
from bs4 import BeautifulSoup
import requests
import datetime





class Command(BaseCommand):
    help = "collect jobs"

    

    def handle(self, *args, **options):
        def setcursandvalute(begin):
            if begin.day > 9:
                d = begin.day
            else:
                d = f'0{begin.day}'
            if begin.month > 9:
                m = begin.month
            else:
                m = f'0{begin.month}'
            
            url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={d}/{m}/{begin.year}'
            print(f"{d}/{m}/{begin.year}")
            responce = requests.get(url)
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

        begin = datetime.datetime.now() - datetime.timedelta(days=1)
        
        while begin:
            setcursandvalute(begin=begin)
            begin = begin - datetime.timedelta(days=1)
            
