# -*- coding: utf-8 -*-
# @Time    : 2018/1/6 14:59
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404