# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, make_response
import pymongo
from models.models import *
from models.database import *
import configparser
import re
import json
from typing import TypedDict

config = configparser.ConfigParser()
config.read('config.ini')
app = Flask( __name__ )
app.secret_key = config.get('LocalPicViewer', 'secret_key')
db_sdata = DBSeriesData()
db_pdata = DBPicData()

PREV = 'prev'
CUR = 'cur'
NEXT = 'next'
PIC_ID = 'pid'
PID_LIST = 'pid_list'
JSON_TEMP = './app/static/cursor_temp.json'

class PidCursor(TypedDict):
    prev: str
    cur: str
    next: str

@app.route('/')
@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/viewer', methods=['GET'])
def view_pic():
    if request.method == 'GET':
        # アドレスからpidを取得し、それを元にDBからデータを取得する
        pid = request.args.get('pic_id', '')
        p_data = db_pdata.load_pic_data(pid)
        series = db_sdata.load_series_data_by_id(p_data.get_series())

        # cookieから自pidの前後のpidを取得する
        # cookie_info = request.cookies.get(PID_LIST)
        f = open(JSON_TEMP, 'r')
        if f is not None:
            cursor_list = json.load(f)
        cursor = None
        title_cursor = {}
        if cursor_list is not None:
            cursor = next(filter(lambda x: x[CUR]==pid, cursor_list), None)
            if cursor is not None:
                title_cursor[PREV] = db_pdata.get_title_by_id(cursor[PREV])
                title_cursor[NEXT] = db_pdata.get_title_by_id(cursor[NEXT])

        response = make_response(render_template('viewer.html',
                                                 pic_data=p_data.get_pic_data(),
                                                 series_title=series.get_series_title(),
                                                 pid_cursor=cursor,
                                                 title_cursor=title_cursor,
                                                 series_page=p_data.get_page()
                                                )
                                )
        cookie_info = {PIC_ID: pid}
        response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
        return response

@app.route('/update_title', methods=['POST'])
def update_title():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]

        if db_pdata.is_id_in_pic_data(pid):
            input_title = request.form[PIC_TITLE]
            db_pdata.update_pic_title(pid, input_title)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/update_rating', methods=['POST'])
def update_star():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]

        if db_pdata.is_id_in_pic_data(pid):
            input_star = request.form[PIC_STAR]
            db_pdata.update_pic_star(pid, int(input_star))

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/update_info', methods=['POST'])
def update_info():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]

        if db_pdata.is_id_in_pic_data(pid):
            input_info = request.form[PIC_INFO]
            db_pdata.update_pic_info(pid, input_info)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/delete_tag', methods=['POST'])
def delete_tags():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]

        if db_pdata.is_id_in_pic_data(pid):
            p_data = db_pdata.load_pic_data(pid)

            # 選択したタグを削除したタグセットを作成する
            tag_list = request.form.getlist('delete_tag')
            set_del_tag = set(tag_list)
            new_tags = p_data.get_tags() - set_del_tag

            if len(list(new_tags)) == 0:
                new_tags = TAG_ZERO

            db_pdata.update_pic_tags(pid, new_tags)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/add_tags', methods=['POST'])
def add_tags():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]
        if db_pdata.is_id_in_pic_data(pid):
            p_data = db_pdata.load_pic_data(pid)
            old_tags = p_data.get_tags()
            old_tags.discard(TAG_ZERO_ITEM)

            # 入力されたタグを加えたセットを作成する
            input_tags = set(re.split(' |,', request.form[PIC_TAG])) - {''}
            new_tags = p_data.get_tags() | input_tags
            if len(list(new_tags)) == 0:
                new_tags = TAG_ZERO

            db_pdata.update_pic_tags(pid, new_tags)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/update_page', methods=['POST'])
def update_page():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]
        if db_pdata.is_id_in_pic_data(pid):
            if db_pdata.is_sid_setting(pid):
                input_page = int(request.form[PIC_SPAGE])
                db_pdata.update_pic_page(pid, input_page)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/update_series', methods=['POST'])
def update_series():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]
        if db_pdata.is_id_in_pic_data(pid):
            input_series = request.form[PIC_SERIES]
            set_series_in_db(pid, input_series)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

def set_series_in_db(pid:str, title:str):
    # 入力されたシリーズタイトルがシリーズDBに無かった時は新規登録
    if not db_sdata.is_title_in_series(title):
        new_series = SeriesData(title)
        sid = new_series.get_sid()
        while True:
            if not db_sdata.is_id_in_series(sid):break
            new_series.set_sid(SeriesData.generate_sid(title, True))
            sid = new_series.get_sid()
        db_sdata.save_series_data(new_series)
    else:
        sid = db_sdata.load_series_data_by_title(title).get_sid()

    return db_pdata.update_pic_series(pid, sid)

# === タグやシリーズを使った検索結果一覧の表示用 ==========================
# idのリストを受け取って双方向リストを作成する
@app.route('/catalog', methods=['GET'])
def catalog():
    tags_list = request.args.getlist('tag')
    sort_order = request.args.get('sort')
    series = request.args.get('series')

    if tags_list is None:
        tags:Set[str]= set()
    else:
        tags = set(tags_list)

    if series is None:
        search_method = 'タグ'

        if sort_order == 'des_rating':
            sort = (PIC_STAR, pymongo.DESCENDING)
        elif sort_order == 'asc_rating':
            sort = (PIC_STAR, pymongo.ASCENDING)
        elif sort_order == 'asc_title':
            sort = (PIC_TITLE, pymongo.ASCENDING)
        elif sort_order == 'des_title':
            sort = (PIC_TITLE, pymongo.DESCENDING)
        elif sort_order == 'acs_path':
            sort = (PIC_PATH, pymongo.ASCENDING)
        elif sort_order == 'des_path':
            sort = (PIC_PATH, pymongo.DESCENDING)
        else:
            return render_template('catalog.html')

        picture_data = db_pdata.search_db_by_tags(tags).sort([sort])

    else:
        if db_sdata.is_title_in_series(series):
            search_method = 'シリーズ'
            sid = db_sdata.load_series_data_by_title(series).get_sid()
            sort = (PIC_SPAGE, pymongo.ASCENDING)
            picture_data = db_pdata.search_db_by_series(sid, tags=tags).sort([sort])
        else:
            return render_template('catalog.html')

    # 検索結果を単純にリスト化する
    result_search = [pdata for pdata in picture_data]

    # 検索結果からpidの双方向リストを作成する
    pid_list = create_pid_list([pdata[DB_ID] for pdata in result_search])
    temp_cursor_file = open(JSON_TEMP, 'w')
    json.dump(pid_list, temp_cursor_file)
    temp_cursor_file.close()
    # cookie_info = {PID_LIST: pid_list}

    # シリーズ名を付加する
    sid_list = sorted(list(set([pdata[PIC_SID] for pdata in result_search])))
    series_dict = {}
    for sid in sid_list:
        series_dict[sid] = db_sdata.load_series_data_by_id(sid).get_series_title()
    for p in result_search:
        p[PIC_SERIES] = series_dict[p[PIC_SID]]

    response = make_response(render_template('catalog.html',
                                             search_method=search_method,
                                             results_search=result_search)
                            )
    #response.set_cookie(PID_LIST, value=json.dumps(cookie_info))

    return response

def create_pid_list(pid_list:List[str]) -> List[PidCursor]:
    return_list: List[PidCursor] = []

    if len(pid_list) == 1:
        pid_cursor: PidCursor = {PREV: pid_list[0],
                                 CUR: pid_list[0],
                                 NEXT: pid_list[0],
                                 }
        return_list.append(pid_cursor)

    elif len(pid_list) == 2:
        pid_cursor: PidCursor = {PREV: pid_list[1],
                                 CUR: pid_list[0],
                                 NEXT: pid_list[1],
                                 }
        return_list.append(pid_cursor)
        pid_cursor: PidCursor = {PREV: pid_list[0],
                                 CUR: pid_list[1],
                                 NEXT: pid_list[0],
                                 }
        return_list.append(pid_cursor)

    elif len(pid_list) > 2:
        pid_cursor: PidCursor = {PREV: pid_list[-1],
                                 CUR: pid_list[0],
                                 NEXT: pid_list[1],
                                 }
        return_list.append(pid_cursor)

        for i in range(1, len(pid_list) - 1):
            pid_cursor: PidCursor = {PREV: pid_list[i-1],
                                     CUR: pid_list[i],
                                     NEXT: pid_list[i+1],
            }
            return_list.append(pid_cursor)

        pid_cursor: PidCursor = {PREV: pid_list[-2],
                                 CUR: pid_list[-1],
                                 NEXT: pid_list[0],
                                 }
        return_list.append(pid_cursor)

    return return_list

@app.route('/search_tag', methods=['POST'])
def search_tags():
    input_tags = list(set(re.split(' |,', request.form[PIC_TAG])) - {''})

    if len(input_tags) == 0:
        tags = None
    elif len(input_tags) > 0:
        tags = input_tags

    sort_order = request.form['sort']

    input_series = request.form[PIC_SERIES]
    if input_series == '':
        series = None
    else:
        series = input_series
        sort_order = None


    return redirect(url_for('catalog',tag=tags, sort=sort_order, series=series))
