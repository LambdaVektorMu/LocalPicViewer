# -*- coding: utf-8 -*-
# データベース接続機能

from pymongo import MongoClient
from models.models import *


class DBSeriesData(object):
    def __init__(self) -> None:
        super().__init__()
        self.client = MongoClient()
        self.db = self.client[LPVDB]
        self.collection = self.db.get_collection(COL_SDATA)

    def save_series_data(self, sid:str, series_title:str):
        return self.collection.insert_one({DB_ID:sid, PIC_SERIES:series_title})

    def load_series_data(self, sid:str):
        db_data = self.collection.find_one(filter={DB_ID:sid})
        return {PIC_SID: db_data[DB_ID], PIC_SERIES: db_data[PIC_SERIES]}

    def is_id_in_series(self, sid:str) -> bool:
        db_data = self.collection.find_one(filter={DB_ID:sid})
        return db_data is not None

class DBPicData(object):
    def __init__(self) -> None:
        super().__init__()
        self.client = MongoClient()
        self.db = self.client[LPVDB]
        self.collection = self.db.get_collection(COL_PDATA)
        self.series_db = DBSeriesData()

    # 1画像のデータを登録
    def save_pic_data(self, pdata:PictureData):
        series = pdata.get_series()
        if not self.series_db.is_id_in_series(series[PIC_SID]):
            self.series_db.save_series_data(sid=series[PIC_SID], series_title=series[PIC_SERIES])

        return self.collection.insert_one(pdata.return_pic_data_noset())

    # IDから1画像のデータを読み込み
    def load_pic_data(self, id:str):
        db_data = self.collection.find_one(filter={DB_ID:id})
        pdata = PictureData(in_id=db_data[DB_ID].lstrip(ID_HEADER),
                            path=db_data[PIC_PATH],
                            title=db_data[PIC_TITLE],
                            tags=set(db_data[PIC_TAG_LIST]),
                            star=db_data[PIC_STAR],
                            info=db_data[PIC_INFO],
                            series_title=db_data[PIC_SERIES],
                            series_page=db_data[PIC_SPAGE])

        return pdata

    # IDがDBに既に登録されているか確認
    def is_id_in_pic_data(self, id:str):
        is_data = self.collection.find_one(filter={DB_ID:id})
        return is_data is not None

    # 画像データのタイトル更新
    def upload_pic_title(self, id:str, title:str):
        filter_id = {DB_ID:id}
        update_title = {'$set': {PIC_TITLE:title}}
        return self.collection.update_one(filter_id, update_title)

    # 画像データの評価更新
    def upload_pic_star(self, id:str, star:int):
        filter_id = {DB_ID:id}
        update_star = {'$set': {PIC_STAR:star}}
        return self.collection.update_one(filter_id, update_star)

    # 画像データのその他情報を更新
    def upload_pic_info(self, id:str, info:str):
        if len(info) <= INFO_LENGTH:
            filter_id = {DB_ID:id}
            update_info = {'$set': {PIC_INFO:info}}
            return self.collection.update_one(filter_id, update_info)

    # 画像データのタグ情報を更新
    def upload_pic_tags(self, id:str, tags:set):
        filter_id = {DB_ID:id}
        update_tags = {'$set': {PIC_TAG:list(tags)}}
        return self.collection.update_one(filter_id, update_tags)

    def search_db_by_tags(self, tags:set={}, sort:str=None):
        tag_list = list(tags)

        if len(tag_list) == 0:
            filter = None
        elif len(tag_list) == 1:
            filter = {PIC_TAG: tag_list[0]}
        else:
            filter_tags = [{PIC_TAG: tag} for tag in tag_list]
            filter = {'$and': filter_tags}

        return self.collection.find(filter=filter)
