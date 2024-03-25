# from lzx
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.util.dir_path import get_parent_path
import pymysql
import os

# 创建app对象
# 更改flask查找模板文件目录
app = Flask(__name__)
# 加载配置文件
app.config.from_pyfile(os.path.join(get_parent_path(__file__, 0), 'config/config.ini'))
# 创建db对象
pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)

# db绑定app
db.init_app(app)
from app.api import book
