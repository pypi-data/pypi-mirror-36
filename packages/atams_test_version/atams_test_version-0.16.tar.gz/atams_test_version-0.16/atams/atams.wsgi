import sys
import os 
import platform

if 'Windows' in platform.platform():
	OS_VER = 'WINDOWS'
elif 'centos' in platform.platform():
	OS_VER = 'CENTOS'
else:
	OS_VER = 'UBUNTU'

if OS_VER == 'WINDOWS':
	CUR_PATH = os.path.join('c:','\ATAMS','atams')
elif OS_VER == 'CENTOS':
	CUR_PATH = '/var/www/html/atams'
	
sys.path.append(CUR_PATH)

from atams import app as application
