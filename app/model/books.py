# from lzx
# coding=gbk
from app import db


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(64), unique=False)
    author = db.Column(db.String(64), unique=False)
    price = db.Column(db.Float, unique=False)