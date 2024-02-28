from django.db import models


class Valute(models.Model):
    unique_id = models.CharField(max_length=20, verbose_name='обозначение')
    num_code = models.IntegerField(verbose_name='числовой код')
    char_code = models.CharField(max_length=3, verbose_name='буквенный код')
    nominal = models.IntegerField(verbose_name='Номинал')
    name = models.CharField(max_length=100, verbose_name='Название валюты')

    def __str__(self):
        return self.name


class Curs(models.Model):
    valute_id = models.ForeignKey('Valute', on_delete=models.CASCADE, verbose_name='Валюта')
    datetime = models.DateTimeField(verbose_name='дата')
    value = models.FloatField(verbose_name='стоимость')

    def __str__(self):
        return f'{self.valute_id.name} {self.datetime} {self.value}'