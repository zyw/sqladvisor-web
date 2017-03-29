#coding=utf-8
from flask import render_template, redirect, session, request, url_for, jsonify
from datetime import datetime
from flask_login import login_user
from .. import db, login_manager
from ..models import User, DatabaseInfo, Analysis
from flask_login import login_required, login_user, current_user
from ..native.sqladvisor import sqladvisor
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
		dbInfos = DatabaseInfo.query.filter_by(user_id = current_user.id)
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
@main.route("/analysis/his", methods=['GET'])
@login_required
def analysis_his():
	analysis_list = Analysis.query.filter_by(user_id=current_user.id)
	return render_template('analysis_his.html',nav='analysis_his',analysis_list = analysis_list)

'''
设置的路由
'''
@main.route("/settings",methods=['POST','GET'])
@login_required
def settings():
	if request.method == 'GET':
		dbInfos = DatabaseInfo.query.all()
		return render_template('settings.html',nav='settings',dbinfos=dbInfos)

	itemName = request.form['itemName']
	dbHost = request.form['dbHost']
	dbPort = request.form['dbPort']
	dbName = request.form['dbName']
	dbUserName = request.form['dbUserName']
	dbPwd = request.form['dbPwd']
	databaseInfo = DatabaseInfo(user_id = current_user.id, 
		item_name = itemName, db_host = dbHost, 
		db_port = dbPort, db_name = dbName, db_user = dbUserName, 
		db_pwd = dbPwd, create_time = datetime.utcnow(), 
		update_time = datetime.utcnow())

	db.session.add(databaseInfo)
	db.session.commit()

	return redirect(url_for('main.settings'))

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