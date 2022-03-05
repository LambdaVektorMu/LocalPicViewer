#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.database import *
from models.models import *
import random
import os

db_sdata = DBSeriesData()
db_pdata = DBPicData()

# db_sdata.save_series_data(SeriesData())

file_list = open('file_list/checked_er18_file_list.txt', 'r')

db_pdata.save_pic_data(PictureData())
for f in file_list:
    file = f.rstrip("\n")
    file_path = ('/'+file.lstrip('./app')).strip()
    file_name = os.path.basename(file_path)
    tags = {file_name, 'exa', 'お試し'}
    star = 0
    info = "test" + str(hash(file_name))
    pdata = PictureData(path=file_path, title=file_name, tags=tags, star=star, info=info)

    while db_pdata.is_id_in_pic_data(pdata.get_id()):
        print(file_path)
        pdata.set_id(PictureData.generate_pid(in_path=file_path, dupe=True))

    db_pdata.save_pic_data(pdata)

file_list.close()
#db_pdata.load_pic_data(pdata.pic_data[PIC_ID])
