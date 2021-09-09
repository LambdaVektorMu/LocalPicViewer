#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.models import *
import configparser
from copy import deepcopy

# === 初期設定 ===============================================
config = configparser.ConfigParser()
config.read('config.ini')
salt = config.get('LocalPicViewer', 'salt')
_hash = Hashids(min_length=ID_LENGTH, salt=salt)

# === テストデータ ============================================
# 何のシリーズでも無い
no_series = SeriesData()
# 何らかのシリーズの場合
SERIES_TITLE2 = '楽しいテスト'
series = SeriesData(SERIES_TITLE2)

# 何も設定していない場合
testdata_0 = PictureData()

# シリーズの設定をしてないケース
PATH1 = '/static/images/nas_pic/SobaCha/EgFQ_giU0AA05rd.jpg'
seed_hash = ''.join(list(reversed(PATH1)))
hashid = _hash.encode(int.from_bytes(seed_hash.encode(), 'big'))
ID1 = hashid[:ID_LENGTH]
TITLE1 = 'test_data_no'
TAGS1 = {'tag'}
STAR1 = 3
INFO1 = 'test'
testdata_no_series = PictureData(path=PATH1,
                                 title=TITLE1,
                                 tags=TAGS1,
                                 star=STAR1,
                                 info=INFO1)

# シリーズの設定をしているケース
PATH2 = '/static/images/nas_pic/SobaCha/EQspibEVAAAFiIT.jpg'
seed_hash = ''.join(list(reversed(PATH2)))
hashid = _hash.encode(int.from_bytes(seed_hash.encode(), 'big'))
ID2 = hashid[:ID_LENGTH]
TITLE2 = 'シリーズあり'
TAGS2 = {'tag1', 'タグ2', '3'}
STAR2 = 5
INFO2 = 'とても楽しいテスト'
SERIES_PAGE2 = 1
testdata_series = PictureData(path=PATH2,
                              title=TITLE2,
                              tags=TAGS2,
                              star=STAR2,
                              info=INFO2,
                              series_title=SERIES_TITLE2,
                              series_page=SERIES_PAGE2)

# ID有 PATH無
id1_path0 = PictureData(in_id=ID1)
# ID有 PATH有
id1_path2 = PictureData(in_id=ID1, path=PATH2)

# === テストケース ============================================
# ID有無×PATH有無の4通り
def test_get_id():
    # ID無 PATH無
    assert testdata_0.get_id() == ID_HEADER + ID_ZERO
    # ID有 PATH無
    assert id1_path0.get_id() != ID_HEADER + ID_ZERO
    assert id1_path0.get_id() == ID_HEADER + ID1
    # ID有 PATH有
    assert id1_path2.get_id() != ID_HEADER + ID_ZERO
    assert id1_path2.get_id() == ID_HEADER + ID1
    assert id1_path2.get_id() != ID_HEADER + ID2
    # ID無 PATH有
    assert testdata_no_series.get_id() != ID_HEADER + ID_ZERO
    assert testdata_no_series.get_id() == ID_HEADER + ID1
    assert testdata_no_series.get_id() != ID_HEADER + ID2
    assert testdata_series.get_id() != ID_HEADER + ID_ZERO
    assert testdata_series.get_id() != ID_HEADER + ID1
    assert testdata_series.get_id() == ID_HEADER + ID2

def test_set_id():
    var_data = deepcopy(testdata_no_series)
    var_data.set_id(ID2)
    assert var_data.get_id() == ID_HEADER + ID2
    assert var_data.get_id() != testdata_no_series.get_id()
    var_data.set_id(ID1+'0')
    assert var_data.get_id() != ID_HEADER + ID1 + '0'
    assert var_data.get_id() == ID_HEADER + ID2

def test_get_path():
    assert testdata_no_series.get_path() == PATH1
    assert testdata_no_series.get_path() != PATH2
    assert testdata_series.get_path() != PATH1
    assert testdata_series.get_path() == PATH2

def test_set_path():
    # ID無 PATH無にPATHを設定
    var_data = deepcopy(testdata_0)
    var_data.set_path(PATH2)
    assert var_data.get_path() == PATH2
    assert var_data.get_id() == ID_HEADER + ID_ZERO
    # ID有 PATH無にPATHを設定
    var_data = deepcopy(id1_path0)
    var_data.set_path(PATH2)
    assert var_data.get_path() == PATH2
    assert var_data.get_id() == ID_HEADER + ID1
    # ID無 PATH有にPATHを設定
    var_data = deepcopy(testdata_no_series)
    assert var_data.get_path() == PATH1
    var_data.set_path(PATH2)
    assert var_data.get_path() == PATH2
    assert var_data.get_path() != PATH1

def test_get_title():
    assert testdata_no_series.get_title() == TITLE1
    assert testdata_no_series.get_title() != TITLE2
    assert testdata_series.get_title() != TITLE1
    assert testdata_series.get_title() == TITLE2

def test_set_title():
    var_data = deepcopy(testdata_no_series)
    assert var_data.get_title() == TITLE1
    var_data.set_title(TITLE2)
    assert var_data.get_title() == TITLE2
    assert var_data.get_title() != TITLE1

def test_get_tags():
    assert testdata_0.get_tags() == TAG_ZERO
    assert testdata_no_series.get_tags() == TAGS1
    assert testdata_series.get_tags() == TAGS2

def test_get_tags_list():
    assert testdata_0.get_tags_list() == sorted(list(TAG_ZERO))
    assert testdata_no_series.get_tags_list() == sorted(list(TAGS1))
    assert testdata_series.get_tags_list() == sorted(list(TAGS2))

def test_set_tags():
    var_data = deepcopy(testdata_0)
    var_data.set_tags(TAGS2)
    assert var_data.get_tags() != TAG_ZERO
    assert var_data.get_tags() == TAGS2
    assert var_data.get_tags_list() == sorted(list(TAGS2))
    var_data = deepcopy(testdata_no_series)
    var_data.set_tags(TAGS2)
    assert var_data.get_tags() != TAGS1
    assert var_data.get_tags() == TAGS2
    assert var_data.get_tags_list() == sorted(list(TAGS2))
    var_data = deepcopy(testdata_series)
    var_data.set_tags(TAGS1)
    assert var_data.get_tags() != TAGS2
    assert var_data.get_tags() == TAGS1
    assert var_data.get_tags_list() == sorted(list(TAGS1))

def test_get_star():
    assert testdata_0.get_star() == STAR_ZERO
    assert testdata_no_series.get_star() == STAR1
    assert testdata_series.get_star() == STAR2

def test_set_star():
    var_data = deepcopy(testdata_no_series)
    var_data.set_star(-1)
    assert var_data.get_star() != -1
    var_data.set_star(0)
    assert var_data.get_star() == 0
    var_data.set_star(1)
    assert var_data.get_star() == 1
    var_data.set_star(2)
    assert var_data.get_star() == 2
    var_data.set_star(3)
    assert var_data.get_star() == 3
    var_data.set_star(4)
    assert var_data.get_star() == 4
    var_data.set_star(5)
    assert var_data.get_star() == 5
    var_data.set_star(6)
    assert var_data.get_star() != 6

def test_get_info():
    assert testdata_0.get_info() == ''
    assert testdata_no_series.get_info() == INFO1
    assert testdata_series.get_info() == INFO2

def test_set_info():
    var_data = deepcopy(testdata_no_series)
    var_data.set_info('')
    assert var_data.get_info() == ''
    var_data.set_info(INFO1)
    assert var_data.get_info() == INFO1
    var_data.set_info('1'*1000)
    assert var_data.get_info() == '1'*1000
    var_data.set_info('2'*1001)
    assert var_data.get_info() != '2'*1001
    assert var_data.get_info() == '1'*1000

def test_get_series():
    series = testdata_0.get_series()
    assert series[PIC_SID] == SID_HEADER + SERIES_NONE_ID
    assert series[PIC_SERIES] == ''
    series = testdata_no_series.get_series()
    assert series[PIC_SID] == SID_HEADER + SERIES_NONE_ID
    assert series[PIC_SERIES] == ''
    series = testdata_series.get_series()
    assert series[PIC_SERIES] == SERIES_TITLE2

def test_set_series():
    var_data = deepcopy(testdata_0)
    var_data.set_series(SERIES_TITLE2)
    series = var_data.get_series()
    s_data = testdata_series.get_series()
    assert series[PIC_SID] != SID_HEADER + SERIES_NONE_ID
    assert series[PIC_SERIES] != ''
    assert series[PIC_SID] == s_data[PIC_SID]
    assert series[PIC_SERIES] == s_data[PIC_SERIES]
    var_data.set_series('')
    series = var_data.get_series()
    assert series[PIC_SID] == SID_HEADER + SERIES_NONE_ID
    assert series[PIC_SERIES] == ''
    assert series[PIC_SID] != s_data[PIC_SID]
    assert series[PIC_SERIES] != s_data[PIC_SERIES]

def test_():
    d = testdata_series.return_pic_data_noset()
    from pprint import pprint
    pprint(d)
