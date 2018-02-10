# -*- coding: utf-8 -*-
# @Time    : 2018/1/6 14:59
# @Author  : liwugang
# @Email   : liwg@olei.me
# @File    : models.py
# @Software: PyCharm
# 存放数据模型
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from _datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员数据模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(100), unique=True)  # 手机号
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    moviecols = db.relationship('Moviecol', backref='user')  # 电影收藏外键关系关联

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    movies = db.relationship('Movie', backref='tag')  # 电影外键关系关联

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 电影标题
    url = db.Column(db.String(255), unique=True)  # 电影播放的url
    info = db.Column(db.Text)  # 电影简介
    logo = db.Column(db.String(255), unique=True)  # 电影的logo
    star = db.Column(db.SmallInteger)  # 电影的星级
    playnum = db.Column(db.BigInteger)  # 电影播放量
    commentnum = db.Column(db.BigInteger)  # 电影的评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 电影所属标签id
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='movie')  # 评论外键关系关联
    moviecols = db.relationship('Moviecol', backref='movie')  # 电影收藏外键关系关联

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 电影标题
    logo = db.Column(db.String(255), unique=True)  # 电影的logo
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影所属ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户所属id
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影所属ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户所属id
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 权限的地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    auths = db.Column(db.String(600))  # 权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin', backref='role')  # 角色外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员名称
    pwd = db.Column(db.String(100), unique=True)  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否是超级管理员,0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 角色ID
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship('Adminlog', backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship('Oplog', backref='admin')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 管理员所属ID
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 管理员所属ID
    ip = db.Column(db.String(100))  # 操作ip
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == "__main__":
    # db.create_all()
    # role = Role(
    #     name="超级管理员",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()
    from werkzeug.security import generate_password_hash

    admin = Admin(
        name="olei",
        pwd=generate_password_hash("olei.me"),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
