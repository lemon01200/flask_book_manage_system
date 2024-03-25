# from lzx
# coding=gbk
#导入wtf表单
from flask_wtf import FlaskForm
#导入自定义表单使用的表单功能
from wtforms import SubmitField, StringField, FloatField


class ViewForm(FlaskForm):
    """html中显示的表单类

    """
    bookname = StringField(label="书名")
    price = FloatField('价格')
    author =  StringField('作者')
    input = SubmitField('提交')