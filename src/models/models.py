# -*- coding: utf-8 -*-
# データベースのテーブルカラム情報を定義する

from hashids import Hashids
import configparser

# DB情報
LPVDB = 'LocalPicViewer'    # DB名
COL_PDATA = 'pic_data'      # 画像情報のコレクション

# 画像情報
PIC_ID = '_id'              # ID
PIC_PATH = 'pic_path'       # その画像の（相対）パス
PIC_TITLE = 'title'         # その画像の独自タイトル
PIC_TAG = 'tags'            # タグ
PIC_STAR = 'rating'         # その画像に対する評判
PIC_INFO = 'information'    # 画像のその他情報
PIC_SID = 'series_id'       # 画像の作品群のユニークID
PIC_SERIES = 'series_title' # 画像の作品群のユニークタイトル
PIC_SPAGE = 'series_page'   # 画像の作品群のページ番号

# 定数
ID_LENGTH = 16                      # IDの長さ
ID_ZERO = '0'*ID_LENGTH             # IDの初期値
STAR_ZERO = -1                      # STARの初期値
TAG_ZERO_ITEM = '未設定'             # TAGに設定さていない時のタグ
TAG_ZERO = {TAG_ZERO_ITEM}          # TAGの初期値
INFO_LENGTH = 1000                  # INFOの長さ
SERIES_NONE_ID = '0'*ID_LENGTH      # シリーズ未設定の場合
SERIES_NONE_PAGE = -1               # シリーズ未設定の場合

config = configparser.ConfigParser()
config.read('config.ini')
salt = config.get('LocalPicViewer', 'salt')
_hash = Hashids(min_length=ID_LENGTH, salt=salt)


class PictureData(object):
    pic_data = {}

    def __init__(self,
                 in_id:str=None,
                 path:str='',
                 title:str='',
                 tags:set=TAG_ZERO,
                 star:int=STAR_ZERO,
                 info:str='',
                 sid:str=None,
                 series_title:str='',
                 series_page:int=SERIES_NONE_PAGE) -> None:
        super().__init__()

        id = in_id
        if in_id is None:
            # IDを付与する
            seed_hash = ''.join(list(reversed(path)))
            hashid = _hash.encode(int.from_bytes(seed_hash.encode(), 'big'))
            id = hashid[:ID_LENGTH]

        series_id = sid
        if sid is None:
            if series_title == '':
                series_id = SERIES_NONE_ID
            else:
                hash_sid = _hash.encode(int.from_bytes(series_title.encode(), 'little'))
                series_id = hash_sid[:ID_LENGTH]

        # 情報を登録する
        self.pic_data[PIC_ID] = id
        self.pic_data[PIC_PATH] = path
        self.pic_data[PIC_TITLE] = title
        self.pic_data[PIC_TAG] = tags
        self.pic_data[PIC_STAR] = star
        self.pic_data[PIC_INFO] = info
        self.pic_data[PIC_SID] = series_id
        self.pic_data[PIC_SERIES] = series_title
        self.pic_data[PIC_SPAGE] = series_page

    def set_id(self, in_id:str):
        if len(in_id) == ID_LENGTH:
            self.pic_data[PIC_ID] = in_id

    def get_id(self):
        return self.pic_data[PIC_ID]

    def set_path(self, in_path:str):
        self.pic_data[PIC_PATH] = in_path

    def get_path(self):
        return self.pic_data[PIC_PATH]

    def set_title(self, in_title:str):
        self.pic_data[PIC_TITLE] = in_title

    def get_title(self):
        return self.pic_data[PIC_TITLE]

    def set_tags(self, in_tags:set):
        self.pic_data[PIC_TAG] = in_tags

    def get_tags(self):
        return self.pic_data[PIC_TAG]

    def set_star(self, in_star:int):
        if in_star >= 0 and in_star <= 5: self.pic_data[PIC_STAR] = in_star

    def get_star(self):
        return self.pic_data[PIC_STAR]

    def set_info(self, in_info:str):
        if len(in_info) <= INFO_LENGTH: self.pic_data[PIC_INFO] = in_info

    def get_info(self):
        return self.pic_data[PIC_INFO]

    def set_series(self, in_series_title:str):
        self.pic_data[PIC_SERIES] = in_series_title

        # シリーズタイトルに合わせてシリーズIDを修正する
        hash_sid = _hash.encode(int.from_bytes(in_series_title.encode(), 'little'))
        self.pic_data[PIC_SID] = hash_sid[:ID_LENGTH]

    def get_series(self):
        return {PIC_SID: self.pic_data[PIC_SID],
                PIC_SERIES: self.pic_data[PIC_SERIES]}

    def set_page(self, page:int):
        self.pic_data[PIC_SPAGE] = page

    def get_page(self):
        return self.pic_data[PIC_SPAGE]

    def convert_tag_list(self):
        return_dict ={}

        return_dict[PIC_ID] = self.pic_data[PIC_ID]
        return_dict[PIC_PATH] = self.pic_data[PIC_PATH]
        return_dict[PIC_TITLE] = self.pic_data[PIC_TITLE]
        return_dict[PIC_TAG] = list(self.pic_data[PIC_TAG])
        return_dict[PIC_STAR] = self.pic_data[PIC_STAR]
        return_dict[PIC_INFO] = self.pic_data[PIC_INFO]
        return_dict[PIC_SID] = self.pic_data[PIC_SID]
        return_dict[PIC_SERIES] = self.pic_data[PIC_SERIES]
        return_dict[PIC_SPAGE] = self.pic_data[PIC_SPAGE]

        return return_dict

def convert_tag_set(data:dict):
    r_data = PictureData(in_id=data[PIC_ID],
                         path=data[PIC_PATH],
                         title=data[PIC_TITLE],
                         tags=set(data[PIC_TAG]),
                         star=data[PIC_STAR],
                         info=data[PIC_INFO],
                         sid=data[PIC_SID],
                         series_title=data[PIC_SERIES],
                         series_page=data[PIC_SPAGE])
    return r_data
