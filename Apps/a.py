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
	#Find zscores of each value relative to the mean and std. dev.
	zcpu = stats.zscore(cpu)
	zmem = stats.zscore(mem)
	#Get the position of the values where the abs. zscore is greater than 2.5 (~97%)
	hcpu = np.array([i for i,n in enumerate(zcpu) if (np.absolute(n) >= 2.5)])
	hmem = np.array([i for i,n in enumerate(zmem) if (np.absolute(n) >= 2.5)])
	#Get where the values for each catagory are within the ~97%
	#spike_pos = [n for n in hcpu,hmem if hcpu[n] == hmem[n]]
	spikes = [x for x,y in zip(hcpu, hmem) if x == y]
	#Graph the zscore for each value.
	fig = Figure()
	gcpu = fig.add_subplot(1, 1, 1)
	gmem = fig.add_subplot(2, 1, 1)
	
	gcpu.plot(cpu)
	gmem.plot(mem)

	FigureCanvasAgg(fig).print_png('webapp.png', dpi=150)
	                                
