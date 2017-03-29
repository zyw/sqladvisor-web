from subprocess import Popen, PIPE
from ..models import DatabaseInfo

def sqladvisor(dbInfo, sqls):
	command = "./app/native/sqladvisor -u %s -p '%s' -P %s -h %s -d %s -q '%s' -v 1" % \
			(dbInfo.db_user, dbInfo.db_pwd, dbInfo.db_port, dbInfo.db_host, dbInfo.db_name, sqls)
	
	return Popen(command, stderr=PIPE, shell=True).stderr.read()