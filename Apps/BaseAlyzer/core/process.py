#  @Author Warosaurus

# ZScore example:
# Source: http://www.wikihow.com/Calculate-Z-Scores

import os
import re
import sqlite3 as sql
import logging as log
import numpy as np
from ftplib import FTP
from scipy import stats
import urllib2 as url
import datetime as dt
import zipfile as z

# Helper methods

# Create a database connection and reutrn it
def db_init(db_location, db_schema):
	con = sql.connect(db_location)
	con.cursor().executescript(open(db_schema, "r").read()) # Pass sql file, execute and commit
	return con # Return cursor object

# Create a ftp connection and reutrn it
def ftp_init(ftp_ip, ftp_username, ftp_password):
	return FTP(ftp_ip).login(ftp_username, ftp_password)

class Process:
	def __init__(self, conf):
		self.conf = conf
		if self.conf.ftp_ip and self.conf.ftp_username and self.conf.ftp_password:
			self.run()
		else:
			log.warning('Configuration could not be created')
			print ("Please view the logs.")

	# Private methods
	# Public mathods
	def run(self):
		log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
		# Create db connection and cursor object
		con = db_init(self.conf.db_dir, self.conf.db_schema)
		cur = con.cursor()
		# Create ftp connection and login
		ftp = ftp_init(self.conf.ftp_ip,self.conf.ftp_username, self.conf.ftp_password)
		# Change ftp directory
		ftp.cwd("datatransport/host01/")
 		# Let's begin!
		# Get date yesterdate
		date_sep = str(dt.date.todate() - dt.timedelta(dates=1))
		date_pln = date_sep.replace('-', '')
		spikes = 0
		events = 0
		# Download all the files for yesterdate
		try:
			flist = [x for x in ftp.nlst()[2:] if re.search(date_sep, x)]
			for x in flist:
				print x # Testing
				with open(conf.files_dir + x, "w+") as f:  # With implies close after loop
					ftp.retrbinary('RETR %s' % n, f.write)
			# Get a list of the files from the directory that matches the date
			flist_dir = [x for x in os.listdir(conf.files_dir) if re.search(date_sep, x)]
			# Baseline first 30 files
			n = 30 # Step at which the window is moved
			start = 0
			end = n
			if (end < len(flist_dir) + 1): # Base line + 1
				while (end < len(flist_dir) - 1): # Needs testing here
					sumCPUn = np.array([])
					sumMemn = np.array([])
					for x in range(start ,end):
						with open(conf.files_dir + flist_dir[x], 'r') as  f:
							sumCPUn.append(sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)]))
							sumMemn.append(sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)]))
					meanCPU = np.mean(sumCPUn)
					meanMem = np.mean(sumMemn)
					stddCPU = np.std(sumCPUn)
					stddMem = np.std(sumMemn)
					# Get next file
					with open(conf.files_dir + flist_dir[end+1], 'r') as f:
						sumCPUnn = sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)])
						sumMemnn = sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)])
					zscoreCPU = (sumCPUnn - meanCPU)/stddCPU
					zscoreMem = (sumMemnn - meanMem)/stddMem
					if ((abs(zscoreCPU) => 2.5) && (abs(zscoreMem) => 2.5)):
						spikes = spikes + 1
					start = start + 1
					end = end + 1 # Get next file
			else:
				log.warning('Error: Not enough files to process - date: {}'.format(date_pln))
			# Deal with events information
			res = url.urlopen('http://data.gdeltproject.org/events/index.html').read().split('<LI>')[4:]
			fil = [x for x in res if (date_pln in x)][0].split('>')[1].split('<')[0]
			# Download events file
			dwnlod = url.urlopen('http://data.gdeltproject.org/events/' + fil)
			with open(conf.files_dir + fil, 'w+') as f:
				f.write(dwnlod.read())
			with z.ZipFile(conf.files_dir + fil) as zf:
				zf.extractall(conf.files_dir)
			# Get all the lines that match
			events = len([x for x in open(conf.files_dir + date_pln + '.export.CSV') if (re.search('Netherlands', x))])
			# Store the results
			with con.cursor() as cur:
				cur.execute('INSERT INTO Results(date, serverId, spikeNum, eventNum, finsished) VALUES(?,?,?,?,?)',	(date_sep, spikes, events))
			con.commit()
		except Exception as e:
			log.warning('Error: {} file: {}'.format(e, x))
		log.info('Processing finished.')
