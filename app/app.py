# coding: utf-8
from flask import Flask, render_template

app = Flask( __name__ )


@app.route('/')
@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/viewer')
def view_pic():
    return render_template('viewer.html')
