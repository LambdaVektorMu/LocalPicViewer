# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from models.models import *
from models.database import *
import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')
app = Flask( __name__ )
app.secret_key = config.get('LocalPicViewer', 'secret_key')
db_sdata = DBSeriesData()
db_pdata = DBPicData()

PREV = 'prev'
NEXT = 'next'
PIC_ID = 'pid'

@app.route('/')
@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/viewer', methods=['GET'])
def view_pic():
    if request.method == 'GET':
        session[PIC_ID] = request.args.get('pic_id', '')
        p_data = db_pdata.load_pic_data(session[PIC_ID])
        return render_template('viewer.html', pic_data=p_data.get_pic_data())

@app.route('/upload_title', methods=['POST'])
def upload_title():
    if db_pdata.is_id_in_pic_data(session[PIC_ID]):
        input_title = request.form[PIC_TITLE]
        db_pdata.upload_pic_title(session[PIC_ID], input_title)
        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))

@app.route('/upload_rating', methods=['POST'])
def upload_star():
    if db_pdata.is_id_in_pic_data(session[PIC_ID]):
        input_star = request.form[PIC_STAR]
        db_pdata.upload_pic_star(session[PIC_ID], int(input_star))
        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))

@app.route('/upload_info', methods=['POST'])
def upload_info():
    if db_pdata.is_id_in_pic_data(session[PIC_ID]):
        input_info = request.form[PIC_INFO]
        db_pdata.upload_pic_info(session[PIC_ID], input_info)
        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))

@app.route('/delete_tag', methods=['POST'])
def delete_tags():
    if db_pdata.is_id_in_pic_data(session[PIC_ID]):
        p_data = db_pdata.load_pic_data(session[PIC_ID])

        # 選択したタグを削除したタグセットを作成する
        tag_list = request.form.getlist('delete_tag')
        set_del_tag = set(tag_list)
        new_tags = p_data.get_tags() - set_del_tag

        if len(list(new_tags)) == 0:
            new_tags = TAG_ZERO

        db_pdata.upload_pic_tags(session[PIC_ID], new_tags)

        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))

@app.route('/add_tags', methods=['POST'])
def add_tags():
    if db_pdata.is_id_in_pic_data(session[PIC_ID]):
        p_data = db_pdata.load_pic_data(session[PIC_ID])
        old_tags = p_data.get_tags()
        old_tags.discard(TAG_ZERO_ITEM)

        # 入力されたタグを加えたセットを作成する
        input_tags = set(re.split(' |,', request.form[PIC_TAG])) - {''}
        new_tags = p_data.get_tags() | input_tags
        if len(list(new_tags)) == 0:
            new_tags = TAG_ZERO

        db_pdata.upload_pic_tags(session[PIC_ID], new_tags)

        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))

@app.route('/catalog', methods=['POST', 'GET'])
def catalog():
    return render_template('catalog.html')

@app.route('/search_tag', methods=['POST'])
def search_tags():
    input_tags = set(re.split(' |,', request.form[PIC_TAG])) - {''}

    picture_data = db_pdata.search_db_by_tags(input_tags)
    app.logger.debug(list(picture_data))  # debug:タグ検索結果

    return render_template('catalog.html')
