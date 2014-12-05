#!/usr/bin/env python
#@Author Warosaurus

#ZScore example:
#Source: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.mstats.zscore.html
#Matpoltlib example:
#Exmaple: http://matplotlib.org/examples/pylab_examples/webapp_demo.html

import re, numpy as np
from scipy import stats
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

if __name__== "__main__":
	cpu = np.array([int(l.split('= ')[1].split(' ')[0]) for l in open("snmpdump.txt","r") if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)])
	mem = np.array([int(l.split('= ')[1].split(' ')[0]) for l in open("snmpdump.txt","r") if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)])
	print "cpu size: {}".format(len(cpu))
	print "mem size: {}".format(len(mem))
	zcpu = stats.zscore(cpu)
	zmem = stats.zscore(mem)
	
