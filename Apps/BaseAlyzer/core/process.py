#!/usr/bin/env python
#@Author Warosaurus

#ZScore example:
#Source: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.mstats.zscore.html

import os, re
import sqlite3 as sql
import logging as log
import numpy as np
from ftplib import FTP
from scipy import stats

class Process:
	def __init__(self):
		pass

	def run(self, conf):
		log.basicConfig(filename='log.log',level=log.DEBUG,format='%(asctime)s %(message)s',datefmt='%d/%m/%Y %I:%M:%S')
		if conf.i and conf.u and conf.p:
			if os.path.isfile(conf.db):
				#Create db connection and cursor object
				con = sql.connect(conf.db)
				cur = con.cursor()
				#Create ftp connection and login
				ftp = FTP(conf.i)
				ftp.login(conf.u, conf.p)
				#Let's begin!
				#Check the database for the last processed file
				cur.execute('SELECT COUNT(filename) filename FROM processed')
				fcount = cur.fetchone()[0]
				#Change ftp directory *host01*
				ftp.cwd("datatransport/host01/")
				#Get list of files to be processed
				flist = ftp.nlst()[(fcount + 2):] #Number of files processed + 2 (.. .)
				flist = flist[0:1]
				#Process the files
				fname = '/tmp/db/temp.txt'
				for n in flist:
					f = open(fname, 'w+')
					try:
						ftp.retrbinary('RETR %s' % n, f.write)
						f = open(fname, 'r')

						cpu = [l for l in f if re.match('HOST-RESOURCES-MIB::hrSWRunPerfCPU', l)]
						f.seek(0) #Return f to the top of the file
						mem = [l for l in f if re.match('HOST-RESOURCES-MIB::hrSWRunPerfMem', l)]

						if len(cpu) != len(mem):
							log.info('Length of values in memory and cpu are not identical in file: {}'.format(n))
						si = n.split('-')[5][:-5]
						dt = n[:-8]
						#Store file information
						cur.execute('INSERT INTO processed(serverid, filename, datetime) VALUES(?,?,?)',(si,n,dt))
						#Store cpu values
						for l in cpu:
							cur.execute('INSERT INTO results(serverid, category, catNumber, datetime, value) VALUES(?,?,?,?,?)',(si, 'cpu', l.split('.')[1].split(' ')[0], dt, l.split(' = ')[1][:-2]))
						for l in mem:
							cur.execute('INSERT INTO results(serverid, category, catNumber, datetime, value) VALUES(?,?,?,?,?)',(si, 'mem', l.split('.')[1].split(' ')[0], dt, l.split(' = ')[1].split(' ')[0]))
					except Exception as e:
						log.warning('Error: {} file: {}'.format(e,n))
					#Clean up file, ready for next
					os.remove(fname)
				con.close()
				ftp.quit()
			else:
				log.warning('Database could not be found.')
		else:
			log.warning('Configuration could not be created')
		
#if __name__== "__main__":
			#Find zscores of each value relative to the mean and std. dev.
#			zcpu = stats.zscore(cpu)
#			zmem = stats.zscore(mem)
			#Get the position of the values where the abs. zscore is greater than 2.5 (~97%)
#			hcpu = np.array([i for i,n in enumerate(zcpu) if (np.absolute(n) >= 2.5)])
#			hmem = np.array([i for i,n in enumerate(zmem) if (np.absolute(n) >= 2.5)])
			#Get where the values for each catagory are within the ~97%
#			spikes = [x for x,y in zip(hcpu, hmem) if x == y]