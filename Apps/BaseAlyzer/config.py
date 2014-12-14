#!/usr/bin/env python
#@Author Warosaurus

import os.path

class config:
	
	def __init__(self):
		self.i = ""
		self.u = ""
		self.p = ""	
		if os.path.isfile(".auth"):
			f = open(".auth", "r").readlines()
			self.i = f[0].split(':')[1]
			self.u = f[1].split(':')[1]
			self.p = f[2].split(':')[1]

if __name__ == "__main__":
	c = config()
	print c.i + c.u + c.p