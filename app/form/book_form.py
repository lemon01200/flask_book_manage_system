# from lzx
# coding=gbk
#����wtf��
from flask_wtf import FlaskForm
#�����Զ����ʹ�õı�����
from wtforms import SubmitField, StringField, FloatField


class ViewForm(FlaskForm):
    """html����ʾ�ı���

    """
    bookname = StringField(label="����")
    price = FloatField('�۸�')
    author =  StringField('����')
    input = SubmitField('�ύ')