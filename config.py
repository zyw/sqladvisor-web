#-*- coding=utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS=True
	POSTS_PER_PAGE=15
	# MYSQL_DATABASE_HOST	= '127.0.0.1'
	# MYSQL_DATABASE_PORT	= 3306
	# MYSQL_DATABASE_USER	= 'root'
	# MYSQL_DATABASE_PASSWORD	= 'root'
	# MYSQL_DATABASE_DB = 'sqladvisor'
	# MYSQL_DATABASE_CHARSET = 'utf8'

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:root@localhost/sqladvisor'

config = {
 'development': DevelopmentConfig,
 # 'testing': TestingConfig,
 # 'production': ProductionConfig,
 'default': DevelopmentConfig
}
