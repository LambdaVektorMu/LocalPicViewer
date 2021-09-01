#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.database import *
from models.models import *
import os

db_pdata = DBPicData(LPVDB, COL_PDATA)
print(db_pdata.search_id_pic_data(ID_ZERO))
print(db_pdata.search_id_pic_data('00000001'))

file_path = '/'+('./app/static/images/nas_pic/SobaCha/EgFRAQBUYAAwo7T.jpg'.lstrip('./app'))
file_name = os.path.basename(file_path)
tags = {'exa', '例'}
star = 1
info = 'お試し'
pdata = PictureData(path=file_path, title=file_name, tags=tags, star=star, info=info)
from pprint import pprint
pprint(pdata.pic_data)
#db_pdata.save_pic_data(pdata)
db_pdata.load_pic_data(pdata.pic_data[PIC_ID])
