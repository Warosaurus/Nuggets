#!/usr/bin/env python
#@Author Warosaurus

import os.path

class Config:
	def __init__(self):
		self.i, self.u, self.p = "","","" #Defaults
		self.db = "/tmp/db/base.db"
		if os.path.isfile(".auth"):
			f = open(".auth", "r").readlines()
			self.i = f[0].split(':')[1].strip()
			self.u = f[1].split(':')[1].strip()
			self.p = f[2].split(':')[1].strip()