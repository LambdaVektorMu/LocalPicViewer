#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.database import *
from models.models import *
import random
import os
from typing import List

db_sdata = DBSeriesData()
db_pdata = DBPicData()

twitter: List[SeriesData] = []
twitter.append(SeriesData('Twitter'))
twitter.append(SeriesData('ツイッター'))
db_sdata.save_series_data(SeriesData())
db_sdata.save_series_data(twitter[0])
db_sdata.save_series_data(twitter[1])

f = open('sobacha_file_list.txt', 'r')

db_pdata.save_pic_data(PictureData())
for i in range(10):
    file = f.readline()
    file_path = ('/'+file.lstrip('./app')).strip()
    file_name = os.path.basename(file_path)
    tags = {file_name, 'exa', 'お試し'}
    star = random.randint(0, 5)
    info = str(hash(file_name))
    pdata = PictureData(path=file_path, title=file_name, tags=tags, star=star, info=info)
    if i%3 != 0: pdata.set_series(twitter[i%3 - 1].get_sid())
    db_pdata.save_pic_data(pdata)

f.close()
#db_pdata.load_pic_data(pdata.pic_data[PIC_ID])
