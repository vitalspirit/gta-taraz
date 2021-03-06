from django.db import models


class Gtu(models.Model):
    gg_manufacturer = models.CharField('Производитель', max_length = 200)
    gg_model = models.CharField('Модель газогенератора', max_length = 200)
    gg_power = models.CharField('Мощность газогенератора', max_length = 200)
    gg_compression = models.CharField('Степень сжатия', max_length = 200)
    gg_rpm_lp = models.CharField('Скорость вращения ТНД', max_length = 200)
    gg_rpm_hp = models.CharField('Скорость вращения ТВД', max_length = 200)
    gg_efficiency = models.CharField('КПД газогенератора', max_length = 200)
    gg_mass = models.CharField('Масса газогенератора', max_length = 200)
    gg_synt_oil_type = models.CharField('Тип синтетического масла', max_length = 200)
    gg_synt_oil_tank = models.CharField('Объем бака синтетического масла', max_length = 200)
    pt_manufacturer = models.CharField('Производитель Силовой Турбины', max_length = 200, null = True)

    def __str__(self):
        return self.gg_model



class Station(models.Model):
    name = models.CharField('Название компрессорной станции', max_length = 200)
    gtu_number = models.CharField('Количество ГПА', max_length = 2)
    gtu_type = models.ForeignKey(Gtu, on_delete = models.CASCADE)

    def __str__(self):
        return self.name




class Shutdown(models.Model):
    SD_CHOICES = [
        ('АВТО', 'АВТО'),
        ('ВНО', 'ВНО'),
    ]
    sd_type = models.CharField('Тип останова', max_length = 50, choices = SD_CHOICES)
    station = models.ForeignKey(Station, on_delete = models.CASCADE)
    gtu = models.CharField('ГПА №', max_length = 10)
    datetime = models.DateTimeField('Дата и время останова')
    act_number = models.CharField('Акт расследования', max_length = 3)
    desc = models.TextField('Причина останова')
    sd_act = models.FileField(upload_to = 'static/images/')
    created = models.DateTimeField(auto_now_add=True)
    detailed_desc = models.TextField('Подробное описание останова и проведенных мероприятий', blank = True)

    def __str__(self):
        a = str(self.station)+'  '+str(self.datetime)
        return a

class W_hours(models.Model):
    YEAR_CHOICES = [
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
    ]
    year = models.CharField(max_length = 4, choices = YEAR_CHOICES)
    station = models.ForeignKey(Station, on_delete = models.CASCADE, null = True)
    gtu = models.CharField('ГПА', max_length = 10, blank = True)
    w_hours = models.CharField('Наработка в часах', max_length = 5, blank = True)
    year_hours = models.CharField('Количество часов в году', max_length = 6, blank = True)

    def __str__(self):
        a = str(self.year)+'  '+str(self.station)+'  '+str(self.gtu)
        return a
