#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.models import *
import configparser
from copy import deepcopy
import pytest

# === 初期設定 ===============================================
config = configparser.ConfigParser()
config.read('config.ini')
salt = config.get('LocalPicViewer', 'salt')
p_hash = Hashids(min_length=PID_LENGTH, salt=salt)
s_hash = Hashids(min_length=SID_LENGTH, salt=salt)

# +++ SeriesData ++++++++++++++++++++++++++++++++++++++++++++
# === テストデータ ============================================
# 何のシリーズでも無い
no_series = SeriesData()
# 何らかのシリーズの場合
SERIES_TITLE2 = '楽しいテスト'
series = SeriesData(SERIES_TITLE2)

# === テストケース ============================================
def test_generate_sid():
    assert SeriesData.generate_sid() == SID_HEADER + SERIES_NONE_ID
    sid = SeriesData.generate_sid(SERIES_TITLE2)
    print('generated sid:', sid)
    assert sid == series.series_data[DB_ID]
    sid = SeriesData.generate_sid(SERIES_TITLE2, dupe=True)
    print('generated sid:', sid)
    assert sid != series.series_data[DB_ID]
    with pytest.raises(ValueError): SeriesData.generate_sid(series_title='', dupe=True)

def test_get_sid():
    assert no_series.get_sid() == SID_HEADER + SERIES_NONE_ID
    assert series.get_sid() == SeriesData.generate_sid(SERIES_TITLE2)

def test_set_sid():
    testdata_no = deepcopy(no_series)
    assert testdata_no.get_sid() == no_series.get_sid()
    testdata_no.set_sid(SeriesData.generate_sid(SERIES_TITLE2))
    assert testdata_no.get_sid() != no_series.get_sid()
    assert testdata_no.get_sid() == series.get_sid()
    testdata_no.set_sid(SeriesData.generate_sid(SERIES_TITLE2, dupe=True))
    assert testdata_no.get_sid() != no_series.get_sid()
    assert testdata_no.get_sid() != series.get_sid()

    testdata_series = deepcopy(series)
    assert testdata_series.get_sid() == series.get_sid()
    testdata_series.set_sid(SeriesData.generate_sid())
    assert testdata_series.get_sid() == no_series.get_sid()
    assert testdata_series.get_sid() != series.get_sid()

    testdata_series = deepcopy(series)
    assert testdata_series.get_sid() == series.get_sid()
    test_id = SID_HEADER + '0'*(SID_LENGTH - 1)
    testdata_series.set_sid(test_id)
    assert testdata_series.get_sid() != test_id
    assert testdata_series.get_sid() == series.get_sid()
    test_id = SID_HEADER + '0'*(SID_LENGTH + 1)
    testdata_series.set_sid(test_id)
    assert testdata_series.get_sid() != test_id
    assert testdata_series.get_sid() == series.get_sid()
    test_id = '0'*(ALL_SID_LENGTH)
    testdata_series.set_sid(test_id)
    assert testdata_series.get_sid() != test_id
    assert testdata_series.get_sid() == series.get_sid()

def test_get_series_title():
    assert no_series.get_series_title() == ''
    assert series.get_series_title() == SERIES_TITLE2

def test_set_series_title():
    testdata_no = deepcopy(no_series)
    assert testdata_no.get_series_title() == no_series.get_series_title()
    testdata_no.set_series_title(SERIES_TITLE2)
    assert testdata_no.get_series_title() != no_series.get_series_title()
    assert testdata_no.get_series_title() == series.get_series_title()

    testdata_series = deepcopy(series)
    assert testdata_series.get_series_title() == series.get_series_title()
    testdata_series.set_series_title('あああ')
    assert testdata_series.get_series_title() != series.get_series_title()

# +++ PictureData ++++++++++++++++++++++++++++++++++++++++++++
# === テストデータ ============================================
# 何も設定していない場合
testdata_0 = PictureData()

# シリーズの設定をしてないケース
PATH1 = '/static/images/nas_pic/SobaCha/EgFQ_giU0AA05rd.jpg'
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
                              series_id=series.get_sid(),
                              series_page=SERIES_PAGE2)

# === テストケース ============================================
def test_generate_pid():
    assert PictureData.generate_pid() == PID_HEADER + PID_ZERO
    pid = PictureData.generate_pid(PATH1)
    print('generated pid:', pid)
    assert pid == testdata_no_series.pic_data[DB_ID]
    pid = PictureData.generate_pid(PATH1, dupe=True)
    print('generated pid:', pid)
    assert pid != testdata_no_series.pic_data[DB_ID]
    with pytest.raises(ValueError): PictureData.generate_pid(in_path='', dupe=True)

def test_get_id():
    assert testdata_0.get_id() == PictureData.generate_pid()
    assert testdata_no_series.get_id() == PictureData.generate_pid(PATH1)
    assert testdata_series.get_id() == PictureData.generate_pid(PATH2)

def test_set_id():
    var_data = deepcopy(testdata_no_series)
    var_data.set_id(PictureData.generate_pid(PATH2))
    assert var_data.get_id() != PictureData.generate_pid(PATH1)
    assert var_data.get_id() == PictureData.generate_pid(PATH2)
    var_data.set_id(PictureData.generate_pid(PATH2, dupe=True))
    assert var_data.get_id() != PictureData.generate_pid(PATH2)

    var_data.set_id(PictureData.generate_pid(PATH2))
    test_id = PID_HEADER + '0'*(PID_LENGTH - 1)
    var_data.set_id(test_id)
    assert var_data.get_id() != test_id
    assert var_data.get_id() == PictureData.generate_pid(PATH2)
    test_id = PID_HEADER + '0'*(PID_LENGTH + 1)
    var_data.set_id(test_id)
    assert var_data.get_id() != test_id
    assert var_data.get_id() == PictureData.generate_pid(PATH2)
    test_id = '0'*(ALL_PID_LENGTH)
    var_data.set_id(test_id)
    assert var_data.get_id() != test_id
    assert var_data.get_id() == PictureData.generate_pid(PATH2)

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
    assert testdata_0.get_series() == SID_HEADER + SERIES_NONE_ID
    assert testdata_no_series.get_series() == SID_HEADER + SERIES_NONE_ID
    assert testdata_series.get_series() == SeriesData.generate_sid(SERIES_TITLE2)

def test_set_series():
    var_data = deepcopy(testdata_no_series)
    var_data.set_series(SeriesData.generate_sid(TITLE2))
    assert var_data.get_series() != SID_HEADER + SERIES_NONE_ID
    assert var_data.get_series() == SeriesData.generate_sid(TITLE2)
    var_data.set_series(SeriesData.generate_sid())
    assert var_data.get_series() != SeriesData.generate_sid(TITLE2)
    assert var_data.get_series() == SID_HEADER + SERIES_NONE_ID

    test_id = SID_HEADER + '0'*(SID_LENGTH - 1)
    var_data.set_series(test_id)
    assert var_data.get_series() == SID_HEADER + SERIES_NONE_ID
    test_id = SID_HEADER + '0'*(SID_LENGTH + 1)
    var_data.set_series(test_id)
    assert var_data.get_series() == SID_HEADER + SERIES_NONE_ID
    test_id = '0'*(ALL_SID_LENGTH)
    var_data.set_series(test_id)
    assert var_data.get_series() == SID_HEADER + SERIES_NONE_ID
