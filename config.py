# @Author Warosaurus

import os.path
import logging as log


class Config:
	def __init__(self):
		self.ftp_ip, self.ftp_username, self.ftp_password = "", "", ""  # Defaults
		self.dir_dbs = "files/db/base.db"
		self.dir_tmp = "files/tmp/"
		self.dir_arc = "files/archives/"
		self.dir_dwl = "files/downloads/"
		# Database Schema
		self.dbs_schema = "schema.sql"
		# Get ftp settings from .auth file
		if os.path.isfile(".auth"):
			f = open(".auth", 'r').readlines()
			self.ftp_ip = f[0].split(':')[1].strip()
			self.ftp_username = f[1].split(':')[1].strip()
			self.ftp_password = f[2].split(':')[1].strip()
		else:
			print ("Auth file is being created. Please fill in the details")
			with open(".auth", "w+") as f:
				f.write("ip:")
				f.write("username:")
				f.write("password:")
