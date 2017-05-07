#-*- coding=utf-8 -*-
import os
from flask import render_template, redirect, session, request, url_for, jsonify, flash
from datetime import datetime
from flask_login import login_user, logout_user
from .. import db, login_manager
from ..models import User, DatabaseInfo, Analysis
from flask_login import login_required, login_user, current_user
from ..native.sqladvisor import sqladvisor

from config import config
from . import main

login_manager.login_view = 'main.login'

'''
首页路由
'''
@main.route("/")
def index():
	return render_template('index.html',nav='home')

'''
分析路由
'''
@main.route("/analysis", methods=['POST', 'GET'])
@login_required
def analysis():
	if request.method == 'GET':
		dbInfos = DatabaseInfo.query.filter_by(user_id = current_user.id, status = 1)
		return render_template('analysis.html',nav='analysis',dbinfos = dbInfos)

	try:
		dbInfoId = request.form['dbInfoId']
		sqls = request.form['sqls']
		dbInfo = DatabaseInfo.query.get(dbInfoId)
		result = sqladvisor(dbInfo,sqls)
		#保存分析结果
		analysis = Analysis(dbinfo_id=dbInfoId, user_id=current_user.id, 
			dbinfo_name=dbInfo.item_name, original_sql = sqls, analysis_result='', create_time=datetime.utcnow())
		db.session.add(analysis)
		db.session.commit()
		return result
	except:
		return '分析失败，请在sql语句末尾添加分号！'

'''
分析历史列表
'''
@main.route("/analysis/his/<page>", methods=['GET'])
@login_required
def analysis_his(page):
	POSTS_PER_PAGE = config[os.getenv('FLASK_CONFIG') or 'default'].POSTS_PER_PAGE
	analysis_list = Analysis.query.filter_by(user_id=current_user.id).paginate(int(page),POSTS_PER_PAGE,False)
	return render_template('analysis_his.html',nav='analysis_his',analysis_list = analysis_list)

'''
数据库设置
根据ID完成新增和编辑功能
'''
@main.route("/settings", methods=['POST','GET'])
@login_required
def settings():
	if request.method == 'GET':
		dbInfos = DatabaseInfo.query.filter_by(user_id = current_user.id, status = 1)
		return render_template('settings.html',nav='settings',dbinfos=dbInfos)

	id = request.form['id']
	itemName = request.form['itemName']
	dbHost = request.form['dbHost']
	dbPort = request.form['dbPort']
	dbName = request.form['dbName']
	dbUserName = request.form['dbUserName']
	dbPwd = request.form['dbPwd']
	databaseInfo = DatabaseInfo(user_id = current_user.id, 
		item_name = itemName, db_host = dbHost, 
		db_port = dbPort, db_name = dbName, db_user = dbUserName, 
		db_pwd = dbPwd, status=1, create_time = datetime.utcnow(), 
		update_time = datetime.utcnow())

	if(id != '0'):
		databaseInfo = DatabaseInfo.query.get(id)
		databaseInfo.item_name = itemName
		databaseInfo.db_host = dbHost
		databaseInfo.db_port = dbPort
		databaseInfo.db_name = dbName
		databaseInfo.db_user = dbUserName
		databaseInfo.db_pwd = dbPwd
		databaseInfo.update_time = datetime.utcnow()

	db.session.add(databaseInfo)
	db.session.commit()

	return redirect(url_for('main.settings'))

@main.route("/settings/<settings_id>/del", methods=['GET'])
def settings_del(settings_id):
	databaseInfo = DatabaseInfo.query.get(settings_id)
	databaseInfo.status = 0

	db.session.add(databaseInfo)
	db.session.commit()

	return jsonify({'code': 10003, 'success': True, 'message': 'deleted success! '})
'''
验证配置名称是否重复
'''
@main.route('/validate/item/name', methods=['POST'])
def validate_item_name():
	valid = True
	itemName = request.form['itemName']
	dbinfo_count = DatabaseInfo.query.filter_by(item_name=itemName).count()
	if(dbinfo_count > 0):
		valid = False
	return jsonify({'valid': valid})

@main.route("/login",methods=['POST','GET'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	if request.method == 'POST':
		username = request.form['username']
		pwd = request.form['pwd']
		rememberMe = request.form['rememberMe']

		user = User.query.filter_by(username = username).first()

		if user is not None and user.password == pwd:
			login_user(user, rememberMe)
			return jsonify({'code': 10002, 'success': True, 'message': 'login success! '})

		return jsonify({'code': 10001, 'success': False, 'message': 'login failure! '})

@main.route("/logout")
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@main.route("/register", methods=['POST','GET'])
def register():
	if request.method == 'GET':
		return render_template('register.html')

	user_name = request.form['user_name']
	email = request.form['email']
	password = request.form['password']
	confirm_pwd = request.form['confirm_pwd']

	user = User(username=user_name, password=password, email=email, avatar='', status=1, create_time=datetime.utcnow(), update_time=datetime.utcnow())

	db.session.add(user)
	db.session.commit()

	return redirect(url_for('main.login'))


