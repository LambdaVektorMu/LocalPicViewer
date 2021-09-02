# -*- coding: utf-8 -*-
from types import MethodDescriptorType
from flask import Flask, render_template, request, redirect, url_for, session
from models.models import *
from models.database import *
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
app = Flask( __name__ )
app.secret_key = config.get('LocalPicViewer', 'secret_key')
db_pdata = DBPicData(LPVDB, COL_PDATA)


@app.route('/')
@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/viewer', methods=['POST', 'GET'])
def view_pic():
    if request.method == 'GET':
        session[PIC_ID] = request.args.get('pic_id', '')
        p_data = db_pdata.load_pic_data(session[PIC_ID])
        return render_template('viewer.html', pic_data=p_data.convert_tag_list())
    #elif request.method == 'POST':

@app.route('/upload_title', methods=['POST'])
def upload_title():
    if db_pdata.search_id_pic_data(session[PIC_ID]):
        input_title = request.form[PIC_TITLE]
        db_pdata.upload_pic_title(session[PIC_ID], input_title)
        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))

@app.route('/upload_rating', methods=['POST'])
def upload_star():
    if db_pdata.search_id_pic_data(session[PIC_ID]):
        input_star = request.form[PIC_STAR]
        db_pdata.upload_pic_star(session[PIC_ID], input_star)
        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))

@app.route('/upload_info', methods=['POST'])
def upload_info():
    if db_pdata.search_id_pic_data(session[PIC_ID]):
        input_info = request.form[PIC_INFO]
        db_pdata.upload_pic_info(session[PIC_ID], input_info)
        return redirect(url_for('view_pic', pic_id=session[PIC_ID]))
