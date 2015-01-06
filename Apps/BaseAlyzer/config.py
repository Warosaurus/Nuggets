#!/usr/bin/env python
# @Author Warosaurus

import os.path
import logging as log

class Config:
	def __init__(self):
		self.ftp_ip, self.ftp_username, self.ftp_password = "","","" #Defaults
		self.db_dir = "/var/db/base.db"
		self.db_schema = "schema.sql"
		self.files_dir = "/var/db/files/"
		self.plot_dir = '../../Plot'
		if os.path.isfile(".auth"):
			f = open(".auth", 'r').readlines()
			self.ftp_ip = f[0].split(':')[1].strip()
			self.ftp_username = f[1].split(':')[1].strip()
			self.ftp_password = f[2].split(':')[1].strip()
