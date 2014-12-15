#!/usr/bin/env python
#@Author Warosaurus

import numpy as np
import sqlite3 as sql
from scipy import stats
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

class Visualize:
	def __init__(self):
		pass
	
	def run(self, db):
		#Connect to db
#		con = sql.connect(conf.db)
		con = sql.connect('/var/db/base.db')
		cur = con.cursor()
		#Visual 1: scatterplot - zscore of all values from cat regardless of CatNumber
		#Get the values
		cpu = cur.execute('SELECT value FROM results WHERE category IS "cpu"')
		print cpu.fetchone()
		
		#Find zscores of each value relative to the mean and std. dev.
#		zcpu = stats.zscore(cpu)
#		zmem = stats.zscore(mem)
		#Get the position of the values where the abs. zscore is greater than 2.5 (~97%)
#		hcpu = np.array([i for i,n in enumerate(zcpu) if (np.absolute(n) >= 2.5)])
#		hmem = np.array([i for i,n in enumerate(zmem) if (np.absolute(n) >= 2.5)])
		#Get where the values for each catagory are within the ~97%
#		spikes = [x for x,y in zip(hcpu, hmem) if x == y]

#Testing
if __name__ == "__main__":
	vis = Visualize()
	vis.run('/var/db/base.db')