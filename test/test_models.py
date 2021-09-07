#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.models import *
from copy import deepcopy

PATH1 = '/static/images/nas_pic/SobaCha/EgFQ_giU0AA05rd.jpg'
TITLE1 = 'test_data_no'
TAGS1 = {'tag'}
STAR1 = 3
INFO1 = 'test'

PATH2 = '/static/images/nas_pic/SobaCha/EQspibEVAAAFiIT.jpg'
TITLE2 = 'シリーズあり'
TAGS2 = {'tag1', 'タグ2', '3'}
STAR2 = 5
INFO2 = 'とても楽しいテスト'
SERIES_TITLE2 = '楽しいテスト'
SERIES_PAGE2 = 1

testdata_0 = PictureData()      # 何も設定していない場合
testdata_no_series = PictureData(path=PATH1,
                                 title=TITLE1,
                                 tags=TAGS1,
                                 star=STAR1,
                                 info=INFO1)

testdata_series = PictureData(path=PATH2,
                              title=TITLE2,
                              tags=TAGS2,
                              star=STAR2,
                              info=INFO2,
                              series_title=SERIES_TITLE2,
                              series_page=SERIES_PAGE2)

def test_get_path_no_series1():
    assert testdata_no_series.get_path == PATH1

def test_get_path_no_series2():
    assert testdata_no_series.get_path != PATH2
