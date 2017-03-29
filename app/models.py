#coding=utf-8
from flask_login import UserMixin
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, index=True)
	password = db.Column(db.String(200))
	email = db.Column(db.String(100),unique=True,index=True)
	avatar = db.Column(db.String(200))
	status = db.Column(db.Integer)
	create_time = db.Column(db.DateTime)
	update_time = db.Column(db.DateTime)

class DatabaseInfo(db.Model):
	__tablename__ = 'database_info'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
 	item_name = db.Column(db.String(50))
 	db_host = db.Column(db.String(100))
 	db_port = db.Column(db.Integer, default=3306)
 	db_name = db.Column(db.String(50))
 	db_user = db.Column(db.String(50))
 	db_pwd = db.Column(db.String(50))
 	create_time = db.Column(db.DateTime)
 	update_time = db.Column(db.DateTime)

class Analysis(db.Model):
	__tablename__ = 'analysis'
	id = db.Column(db.Integer, primary_key=True)
  	dbinfo_id = db.Column(db.Integer)             #数据库配置ID
  	user_id = db.Column(db.Integer) 			  #用户ID
  	dbinfo_name = db.Column(db.String(50))		  #数据库配置名称
  	original_sql = db.Column(db.String(2000))        #原SQL语句
  	analysis_result = db.Column(db.Text)				#分析结果
  	create_time = db.Column(db.DateTime)			#创建时间