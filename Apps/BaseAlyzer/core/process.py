#@Author Warosaurus

#ZScore example:
#Source: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.mstats.zscore.html

import os, re
import sqlite3 as sql
import logging as log
import numpy as np
from ftplib import FTP
from scipy import stats
import urllib2 as url
import datetime as dt
import zipfile as z

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
				#Get date yesterday 5
				dayz = [str(dt.date.today() - dt.timedelta(days=x)) for x in list(reversed(range(2,7)))] #Test
				for day_sep in dayz:
					print day_sep
#					day_sep = str(dt.date.today() - dt.timedelta(days=1))
					day_pln = day_sep.replace('-','')
					#Change ftp directory *host01*
					ftp.cwd("datatransport/host01/")
					#Get list of files to be processed
					flist = [x for x in ftp.nlst()[2:] if re.search(day_sep,x)]
					#Process the files
					fname = '/tmp/temp.txt'
					spikes = 0
					log.info('Starting processing for {}.'.format(day_sep))
					for n in flist:
						print (n)
						f = open(fname, 'w+')
#						try:
						#Download the file
						ftp.retrbinary('RETR %s' % n, f.write)
						#Open the file for reading
						f = open(fname, 'r')
						ncpu = np.array([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)])
						f.seek(0) #Return f to the top of the file
						nmem = np.array([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match('HOST-RESOURCES-MIB::hrSWRunPerfMem', l)])
						#Find zscores of each value relative to the mean and std. dev.
						zcpu = stats.zscore(ncpu)
						zmem = stats.zscore(nmem)
						#Get the position of the values where the abs. zscore is greater than 2.5 (~97%)
						hcpu = np.array([i for i,n in enumerate(zcpu) if (np.absolute(n) >= 2.5)])
						hmem = np.array([i for i,n in enumerate(zmem) if (np.absolute(n) >= 2.5)])
						#Get where the values for each catagory are within the ~97%
						spikes = spikes + len([x for x,y in zip(hcpu, hmem) if x == y])
						if len(ncpu) != len(nmem): #Curious to see if there are any files where the number of memory and cpu perf differs
							log.info('Length of values in memory and cpu are not identical in file: {}'.format(n))					
#						except Exception as e:
#							log.warning('Error: {} file: {}'.format(e,n))
						#Clean up file, ready for next
						os.remove(fname)
					#Deal with events information
					res = url.urlopen('http://data.gdeltproject.org/events/index.html').read().split('<LI>')[4:]
					fil = [x for x in res if (day_pln in x)][0].split('>')[1].split('<')[0]
					#Download events file
					dwnlod = url.urlopen('http://data.gdeltproject.org/events/'+fil)
					with open('/tmp/' + fil, 'w+') as f:
						f.write(dwnlod.read())
					with z.ZipFile('/tmp/'+fil) as zf:
						zf.extractall('/tmp/')
					#Get all the lines that match
					events = len([x for x in open('/tmp/'+day_pln+'.export.CSV') if (re.search('Netherlands', x))])
					#Store results
					cur.execute('INSERT INTO Results(date, serverId, spikeNum, eventNum, finsished) VALUES(?,?,?,?,?)',(day_sep,1,spikes,events,1))
					con.commit()
				con.close()
				ftp.quit()
				log.info('Processing finished.')
			else:
				log.warning('Database could not be found.')
				print ("Please view the logs.")
		else:
			log.warning('Configuration could not be created')
			print ("Please view the logs.")
