#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

from models.database import *
from models.models import *

db_sdata = DBSeriesData()
db_pdata = DBPicData()

sids = [SID_HEADER + SERIES_NONE_ID, 'sid_qpLNxrJ2xoDNwOAm', 'sid_DRWz5VNOz9rrevqO']
series_title = ['', 'Twitter', 'ツイッター']

def test_load_series_data_by_id():
    for i, sid in enumerate(sids):
        data = db_sdata.load_series_data_by_id(sid)
        assert data.get_series_title() == series_title[i]

def test_load_series_data_by_title():
    for i, title in enumerate(series_title):
        data = db_sdata.load_series_data_by_title(title)
        assert data.get_sid() == sids[i]

def test_is_id_in_series():
    for sid in sids:
        assert db_sdata.is_id_in_series(sid)

    assert not db_sdata.is_id_in_series(SERIES_NONE_ID)

def test_is_title_in_series():
    for title in series_title:
        assert db_sdata.is_title_in_series(title)

    assert not db_sdata.is_title_in_series('title')