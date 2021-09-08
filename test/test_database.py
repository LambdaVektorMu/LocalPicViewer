#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.database import DBPicData
from models.models import *

db = DBPicData()

testdata00 = PictureData()

PATH1 = '/static/images/nas_pic/SobaCha/EgFQ_giU0AA05rd.jpg'
TITLE1 = 'test_data_no'
TAGS1 = {'tag'}
STAR1 = 3
INFO1 = 'test'
testdata01 = PictureData(path=PATH1,
                         title=TITLE1,
                         tags=TAGS1,
                         star=STAR1,
                         info=INFO1)

PATH2 = '/static/images/nas_pic/SobaCha/EQspibEVAAAFiIT.jpg'
TITLE2 = 'シリーズあり'
TAGS2 = {'tag1', 'タグ2', '3'}
STAR2 = 5
INFO2 = 'とても楽しいテスト'
SERIES_TITLE2 = '楽しいテスト'
SERIES_PAGE2 = 1
testdata02 = PictureData(path=PATH2,
                         title=TITLE2,
                         tags=TAGS2,
                         star=STAR2,
                         info=INFO2,
                         series_title=SERIES_TITLE2,
                         series_page=SERIES_PAGE2)

def test_save_pic_data():
    db.save_pic_data(testdata00)
    db.save_pic_data(testdata01)
    db.save_pic_data(testdata02)

def test_load_pic_data():
    data00 = db.load_pic_data(testdata00.get_id())
    assert data00.get_id() == testdata00.get_id()
    assert data00.get_path() == testdata00.get_path()
    assert data00.get_title() == testdata00.get_title()
    assert data00.get_tags() == testdata00.get_tags()
    assert data00.get_star() == testdata00.get_star()
    assert data00.get_info() == testdata00.get_info()
