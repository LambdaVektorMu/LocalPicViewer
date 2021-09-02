#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.database import *
from models.models import *
import random
import os

db_pdata = DBPicData(LPVDB, COL_PDATA)

f = open('sobacha_file_list.txt', 'r')

for i in range(10):
    file = f.readline()
    file_path = ('/'+file.lstrip('./app')).strip()
    file_name = os.path.basename(file_path)
    tags = {file_name, 'exa', 'お試し'}
    star = random.randint(0, 5)
    info = str(hash(file_name))
    pdata = PictureData(path=file_path, title=file_name, tags=tags, star=star, info=info)
    db_pdata.save_pic_data(pdata)

f.close()
#db_pdata.load_pic_data(pdata.pic_data[PIC_ID])
