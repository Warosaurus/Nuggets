#!/usr/bin/env python
#@Author Warosaurus

from config import Config
from core import Process, Visualize

if __name__ == "__main__":
	c = Config()
	p = Process(c)
#	v = Visualize()
#	v.run(c.db, c.plot) 	# Pass configuration db location
