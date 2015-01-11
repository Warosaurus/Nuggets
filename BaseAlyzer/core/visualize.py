#!/usr/bin/env python
# @Author Warosaurus

import numpy as np
import sqlite3 as sql
from scipy import stats
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

class Visualize:
	def __init__(self, db_location, date):
		self.run(db_location, date)
	
	def run(self, db_location, plot_dir):
		#  Connect to db
		con = sql.connect(db_location)
		cur = con.cursor()
		#  Visual 1: scatterplot - zscore of all values from cat regardless of CatNumber vs datetime
		#  Get the values
		
		#  cpu
		zcpu = [x for x in cur.execute('SELECT zscorecpu FROM Scores WHERE date IS "2014-12-11"').fetchall()]
		dcpu = range(len(zcpu))
		print 'cpu: {}'.format(len(zcpu))
		
		#  mem
		#  Exclude blank results
		zmem = [x for x in cur.execute('SELECT zscoremem FROM Scores WHERE date IS "2014-12-11"').fetchall()]
		dmem = range(len(zmem))
		print 'mem: {}'.format(len(zmem))

		#  Graphing
		figc = Figure()
		figm = Figure()

		ac = figc.add_subplot(1, 1, 1)
		am = figm.add_subplot(1, 1, 1)

		cc = ac.scatter(dcpu, zcpu, 3, c=u'b')
		mc = am.scatter(dmem, zmem, 3, c=u'b')

		FigureCanvasAgg(figc).print_png(plot_dir + '/Plotc.png', dpi=150)
		FigureCanvasAgg(figm).print_png(plot_dir + '/Plotm.png', dpi=150)
		con.close()