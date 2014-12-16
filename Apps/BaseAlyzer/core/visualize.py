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
	
	def run(self, db, plot_dir):
		#TDO test for database existance
		
		#Connect to db
#		con = sql.connect(conf.db)
		con = sql.connect(db)
		cur = con.cursor()
		#Visual 1: scatterplot - zscore of all values from cat regardless of CatNumber vs datetime
		#Get the values
		
		#cpu
		#Exclude blank results
		cpu  = [x for x in cur.execute('SELECT value, datetime FROM results WHERE category IS "cpu"').fetchall() if x[0] != '']
#		dcpu = [str(x[1]) for x in cpu]
		dcpu = range(len(cpu))
		ncpu = np.array([int(x[0]) for x in cpu])
		print 'cpu: {}'.format(len(cpu))
		
		#mem
		#Exclude blank results
		mem  = [x for x in cur.execute('SELECT value, datetime FROM results WHERE category IS "mem"').fetchall() if x[0] != 0]
#		dmem = [str(x[1]) for x in mem]
		dmem = range(len(mem))
		nmem = np.array([x[0] for x in mem])
		print 'mem: {}'.format(len(mem))
		
		#Calculate the zscore for each category
		zcpu = stats.zscore(ncpu)
		zmem = stats.zscore(nmem)

		#Graphing
		figc = Figure()
		figm = Figure()

		ac = figc.add_subplot(1,1,1)
		am = figm.add_subplot(1,1,1)

		cc = ac.scatter(dcpu, zcpu, 3, c=u'b')
		mc = am.scatter(dmem, zmem, 3, c=u'b')

		FigureCanvasAgg(figc).print_png(plot_dir + '/Plotc.png', dpi=150)
		FigureCanvasAgg(figm).print_png(plot_dir + '/Plotm.png', dpi=150)
		
		#Find zscores of each value relative to the mean and std. dev.
#		zcpu = stats.zscore(cpu)
#		zmem = stats.zscore(mem)
		#Get the position of the values where the abs. zscore is greater than 2.5 (~97%)
#		hcpu = np.array([i for i,n in enumerate(zcpu) if (np.absolute(n) >= 2.5)])
#		hmem = np.array([i for i,n in enumerate(zmem) if (np.absolute(n) >= 2.5)])
		#Get where the values for each catagory are within the ~97%
#		spikes = [x for x,y in zip(hcpu, hmem) if x == y]
		con.close()

#Testing
if __name__ == "__main__":
	vis = Visualize()
	vis.run('base.db', '../../../Plot')