#!/usr/bin/env python
#@Author Warosaurus

#ZScore example:
#Source: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.mstats.zscore.html

import config
import re, numpy as np
from ftplib import FTP
from scipy import stats

if __name__== "__main__":
	conf = config()
	if conf.i and conf.u and conf.p:
		ftp = FTP(conf.i)
		ftp.login(conf.u, conf.p)
		ftp.cwd("datatransport/host01/")
		
		#TODO
		#Get last checked file
		#Get list of files to be downloaded
		#Go Through file one by one and run algo
		
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
		
		#Go to sleep here
		ftp.quit()
	else:
		print "Config could not be created, please check README."