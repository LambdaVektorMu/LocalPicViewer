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
        # 
        pid = request.args.get('pic_id', '')
        p_data = db_pdata.load_pic_data(pid)
        series = db_sdata.load_series_data_by_id(p_data.get_series())

        #
        cookie_info = cookie_info = request.cookies.get(PID_LIST)
        if cookie_info is not None:
            load_info = json.loads(cookie_info)
            cursor_list = load_info[PID_LIST]
        cursor = None
        if cursor_list is not None:
            cursor = next(filter(lambda x: x[CUR]==pid, cursor_list), None)

        response = make_response(render_template('viewer.html',
                                                 pic_data=p_data.get_pic_data(),
                                                 series_title=series.get_series_title()
                                                )
                                )
        cookie_info = {PIC_ID: pid}
        response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
        return response

@app.route('/upload_title', methods=['POST'])
def upload_title():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]

        if db_pdata.is_id_in_pic_data(pid):
            input_title = request.form[PIC_TITLE]
            db_pdata.upload_pic_title(pid, input_title)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/upload_rating', methods=['POST'])
def upload_star():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]

        if db_pdata.is_id_in_pic_data(pid):
            input_star = request.form[PIC_STAR]
            db_pdata.upload_pic_star(pid, int(input_star))

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

@app.route('/upload_info', methods=['POST'])
def upload_info():
    cookie_info = request.cookies.get(PIC_ID)
    if cookie_info is not None:
        load_info = json.loads(cookie_info)
        pid = load_info[PIC_ID]

        if db_pdata.is_id_in_pic_data(pid):
            input_info = request.form[PIC_INFO]
            db_pdata.upload_pic_info(pid, input_info)

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
            app.logger.debug(tag_list)  # debug
            set_del_tag = set(tag_list)
            new_tags = p_data.get_tags() - set_del_tag
            app.logger.debug(new_tags)  # debug

            if len(list(new_tags)) == 0:
                new_tags = TAG_ZERO

            db_pdata.upload_pic_tags(pid, new_tags)

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

            db_pdata.upload_pic_tags(pid, new_tags)

            response = make_response(redirect(url_for('view_pic', pic_id=pid)))
            cookie_info = {PIC_ID: pid}
            response.set_cookie(PIC_ID, value=json.dumps(cookie_info))
            return response

# === タグやシリーズを使った検索結果一覧の表示用 ==========================
# idのリストを受け取って双方向リストを作成する
@app.route('/catalog', methods=['GET'])
def catalog():
    return render_template('catalog.html')

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
    input_tags = set(re.split(' |,', request.form[PIC_TAG])) - {''}

    sort_order = request.form['sort']
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

    picture_data = db_pdata.search_db_by_tags(input_tags).sort([sort])
    # 検索結果を単純にリスト化する
    result_search = [pdata for pdata in picture_data]
    #app.logger.debug(result_search)  # debug
    # 検索結果からpidの双方向リストを作成する
    pid_list = create_pid_list([pdata[DB_ID] for pdata in result_search])
    app.logger.debug(pid_list)  #debug
    cookie_info = {PID_LIST: pid_list}
    response = make_response(render_template('catalog.html',
                                             search_method='タグ',
                                             results_search=result_search)
                            )
    response.set_cookie(PID_LIST, value=json.dumps(cookie_info))

    #app.logger.debug(pid_list)  # debug:タグ検索結果


    #app.logger.debug(session[PID_LIST])  # debug:タグ検索結果

    return response
