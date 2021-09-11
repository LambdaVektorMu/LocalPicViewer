# -*- coding: utf-8 -*-
# データベースのテーブルカラム情報を定義する

from copy import deepcopy
from random import randint
from hashids import Hashids
import configparser
from typing import Dict, Set, List, TypedDict

# DB情報
LPVDB = 'LocalPicViewer'    # DB名
COL_PDATA = 'pic_data'      # 画像情報のコレクション
COL_SDATA = 'series_data'   # シリーズ情報のコレクション

# 画像情報
DB_ID = '_id'               # DBにおけるユニークなID
PIC_PATH = 'pic_path'       # その画像の（相対）パス
PIC_TITLE = 'title'         # その画像の独自タイトル
PIC_TAG = 'tags'            # タグ
PIC_TAG_LIST = 'tags_list'  # タグのリスト化
PIC_STAR = 'rating'         # その画像に対する評判
PIC_INFO = 'information'    # 画像のその他情報
PIC_SID = 'series_id'       # 画像の作品群のユニークID
PIC_SERIES = 'series_title' # 画像の作品群のユニークタイトル
PIC_SPAGE = 'series_page'   # 画像の作品群のページ番号

# 定数
PID_HEADER = 'pid_'                             # 画像IDのヘッダー
PID_LENGTH = 16                                 # IDの長さ
PID_ZERO = '0'*PID_LENGTH                       # IDの初期値
ALL_PID_LENGTH = len(PID_HEADER) + PID_LENGTH
STAR_ZERO = -1                                  # STARの初期値
TAG_ZERO_ITEM = '未設定'                         # TAGに設定さていない時のタグ
TAG_ZERO = {TAG_ZERO_ITEM}                      # TAGの初期値
INFO_LENGTH = 1000                              # INFOの長さ
SID_HEADER = 'sid_'                             # シリーズIDのヘッダー
SID_LENGTH = 16
SERIES_NONE_ID = '0'*SID_LENGTH                 # シリーズ未設定の場合
ALL_SID_LENGTH = len(SID_HEADER) + SID_LENGTH
SERIES_NONE_PAGE = -1                           # シリーズ未設定の場合

config = configparser.ConfigParser()
config.read('config.ini')
salt = config.get('LocalPicViewer', 'salt')
p_hash = Hashids(min_length=PID_LENGTH, salt=salt)
s_hash = Hashids(min_length=SID_LENGTH, salt=salt)


class SeriesDict(TypedDict):
    _id: str
    series_title: str


class SeriesData(object):

    # シリーズ名からIDを生成する
    @classmethod
    def generate_sid(cls, series_title:str='', dupe:bool=False) -> str:
        if not dupe:
            if series_title == '':
                sid = SERIES_NONE_ID
            else:
                hash_sid = s_hash.encode(int.from_bytes(series_title.encode(), 'little'))
                sid = hash_sid[:SID_LENGTH]
        else:
            if series_title == '':
                raise ValueError
            else:
                hash_sid = s_hash.encode(randint(1, 2**SID_LENGTH) + int.from_bytes(series_title.encode(), 'big'))
                sid = hash_sid[:SID_LENGTH]

        return SID_HEADER + sid

    def __init__(self, series_title:str=''):
        sid = self.generate_sid(series_title=series_title)

        self.series_data: SeriesData = {DB_ID: sid,
                                        PIC_SERIES: series_title}

    # === セッター/ゲッター ===================================
    def set_sid(self, in_sid:str):
        if len(in_sid) == ALL_SID_LENGTH and in_sid[:len(SID_HEADER)] == SID_HEADER:
            self.series_data[DB_ID] = in_sid

    def get_sid(self) -> str:
        return self.series_data[DB_ID]

    def set_series_title(self, in_title:str):
        self.series_data[PIC_SERIES] = in_title

    def get_series_title(self) -> str:
        return self.series_data[PIC_SERIES]


class PictureDict(TypedDict):
    _id: str
    pic_path: str
    title: str
    tags: Set[str]
    tags_list: List[str]
    rating: int
    information: str
    series_id: str
    series_page: int


class PictureData(object):
    # パスからIDを生成する
    @classmethod
    def generate_pid(cls, in_path:str='', dupe:bool=False) -> str:
        if not dupe:
            if in_path == '':
                pid = PID_ZERO
            else:
                seed_hash = ''.join(list(reversed(in_path)))
                hashid = p_hash.encode(int.from_bytes(seed_hash.encode(), 'big'))
                pid = hashid[:PID_LENGTH]
        else:
            if in_path == '':
                raise ValueError
            else:
                seed_hash = ''.join(list(reversed(in_path)))
                hashid = p_hash.encode(randint(1, 2**PID_LENGTH) + int.from_bytes(seed_hash.encode(), 'little'))
                pid = hashid[:PID_LENGTH]

        return PID_HEADER + pid

    def __init__(self,
                 path:str='',
                 title:str='',
                 tags:Set[str]=TAG_ZERO,
                 star:int=STAR_ZERO,
                 info:str='',
                 series_id:str=(SID_HEADER + SERIES_NONE_ID),
                 series_page:int=SERIES_NONE_PAGE):
        self.pic_data: Dict[str, any] = {}
        id = self.generate_pid(in_path=path)

        # 情報を登録する
        if len(series_id) == ALL_SID_LENGTH and series_id[:len(SID_HEADER)] == SID_HEADER:
            setting_series_id = series_id
        else:
            setting_series_id = SeriesData.generate_sid()

        self.pic_data: PictureDict = {DB_ID: id,
                                      PIC_PATH: path,
                                      PIC_TITLE: title,
                                      PIC_TAG: tags,
                                      PIC_TAG_LIST: sorted(list(tags)),
                                      PIC_STAR: star,
                                      PIC_INFO: info,
                                      PIC_SID: setting_series_id,
                                      PIC_SPAGE: series_page
        }

    def set_id(self, in_id:str):
        if len(in_id) == ALL_PID_LENGTH and in_id[:len(PID_HEADER)] == PID_HEADER:
            self.pic_data[DB_ID] = in_id

    def get_id(self) -> str:
        return self.pic_data[DB_ID]

    def set_path(self, in_path:str):
        self.pic_data[PIC_PATH] = in_path

    def get_path(self) -> str:
        return self.pic_data[PIC_PATH]

    def set_title(self, in_title:str):
        self.pic_data[PIC_TITLE] = in_title

    def get_title(self) -> str:
        return self.pic_data[PIC_TITLE]

    def set_tags(self, in_tags:Set[str]):
        self.pic_data[PIC_TAG] = in_tags
        self.pic_data[PIC_TAG_LIST] = sorted(list(in_tags))

    def get_tags(self) -> Set[str]:
        return self.pic_data[PIC_TAG]

    def get_tags_list(self) -> List[str]:
        return self.pic_data[PIC_TAG_LIST]

    def set_star(self, in_star:int):
        if in_star >= 0 and in_star <= 5: self.pic_data[PIC_STAR] = in_star

    def get_star(self) -> int:
        return self.pic_data[PIC_STAR]

    def set_info(self, in_info:str):
        if len(in_info) <= INFO_LENGTH: self.pic_data[PIC_INFO] = in_info

    def get_info(self) -> str:
        return self.pic_data[PIC_INFO]

    def set_series(self, series_id:str):
        if len(series_id) == ALL_SID_LENGTH and series_id[:len(SID_HEADER)] == SID_HEADER:
            self.pic_data[PIC_SID] = series_id

    def get_series(self) -> str:
        return self.pic_data[PIC_SID]

    def set_page(self, page:int):
        self.pic_data[PIC_SPAGE] = page

    def get_page(self) -> int:
        return self.pic_data[PIC_SPAGE]

    def get_pic_data(self):
        return deepcopy(self.pic_data)

    def get_pic_data_noset(self):
        return_data = dict(deepcopy(self.pic_data))
        del return_data[PIC_TAG]
        return return_data
