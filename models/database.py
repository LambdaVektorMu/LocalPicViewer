# -*- coding: utf-8 -*-
# データベース接続機能

from pymongo import MongoClient
from models.models import *


class DBPicData(object):
    def __init__(self, db_name, collection_name) -> None:
        super().__init__()
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db.get_collection(collection_name)

    # 1画像のデータを登録
    def save_pic_data(self, pdata:PictureData):
        insert_data = {
            PIC_ID: pdata.pic_data[PIC_ID],
            PIC_PATH: pdata.pic_data[PIC_PATH],
            PIC_TITLE: pdata.pic_data[PIC_TITLE],
            PIC_TAG: list(pdata.pic_data[PIC_TAG]),
            PIC_STAR: pdata.pic_data[PIC_STAR],
            PIC_INFO: pdata.pic_data[PIC_INFO]
        }
        return self.collection.insert_one(insert_data)

    # IDから1画像のデータを読み込み
    def load_pic_data(self, id:str):
        db_data = self.collection.find_one(filter={PIC_ID:id})
        pdata = PictureData(in_id=db_data[PIC_ID],
                            path=db_data[PIC_PATH],
                            title=db_data[PIC_TITLE],
                            tags=set(db_data[PIC_TAG]),
                            star=db_data[PIC_STAR],
                            info=db_data[PIC_INFO])

        return pdata

    # IDがDBに既に登録されているか確認
    def search_id_pic_data(self, id:str):
        is_data = self.collection.find_one(filter={PIC_ID:id})
        return is_data is not None

    # 画像データのタイトル更新
    def upload_pic_title(self, id:str, title:str):
        filter_id = {PIC_ID:id}
        update_title = {'$set':{PIC_TITLE:title}}
        return self.collection.update_one(filter_id, update_title)

    # 画像データの評価更新
    def upload_pic_star(self, id:str, star:int):
        filter_id = {PIC_ID:id}
        update_star = {'$set':{PIC_STAR:star}}
        return self.collection.update_one(filter_id, update_star)

    # 画像データのその他情報を更新
    def upload_pic_info(self, id:str, info:str):
        if len(info) <= INFO_LENGTH:
            filter_id = {PIC_ID:id}
            update_info = {'$set':{PIC_INFO:info}}
            return self.collection.update_one(filter_id, update_info)
