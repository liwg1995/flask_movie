# -*- coding: utf-8 -*-
# @Time    : 2018/1/6 15:00
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint

admin = Blueprint("admin",__name__)

import app.admin.views