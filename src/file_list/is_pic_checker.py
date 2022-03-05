#!/home/l_vektor_m/venv3.8/bin/python
# -*- coding: utf-8 -*-

# ファイル一覧を読み込んで画像ファイルのみのファイル一覧を新たに生成する。
# python is_pic_checker.py ファイル一覧

import sys
import os
import imghdr

# 引数の数チェック
if len(sys.argv) < 2:
    print("ファイル一覧が指定されていません")
    exit(1)

# ファイル一覧の存在チェック
file_list_arg = sys.argv[1]
if (not os.path.exists(file_list_arg) or
    os.path.isdir(file_list_arg)):
    print("ファイルパスが指定されていません")
    exit(1)

f = open(file_list_arg, "r")
files = f.readlines()
f.close

new_file_list = open("checked_" + file_list_arg, "w")

for f in files:
    file = f.rstrip("\n")
    # ファイルの存在チェック
    if not os.path.exists(file):
        continue
    # ファイルの画像かどうかチェック
    if imghdr.what(file) is None:
        continue

    new_file_list.write(f)

new_file_list.close()
