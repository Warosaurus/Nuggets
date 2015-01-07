#  @Author Warosaurus

# ZScore example:
# Source: http://www.wikihow.com/Calculate-Z-Scores

import os
import re
import sqlite3 as sql
import logging as log
import numpy as np
import datetime as dt


# Create a database connection and reutrn it
def db_init(db_location, db_schema):
	con = sql.connect(db_location)
	con.cursor().executescript(open(db_schema, "r").read())  # Pass sql file, execute and commit
	return con  # Return connection object


class Process:
	def __init__(self, conf, date):
		self.conf = conf
		if self.conf.ftp_ip and self.conf.ftp_username and self.conf.ftp_password:
			self.run(self.conf.files_dir, date)
		else:
			log.warning('Configuration could not be created')
			print ("Please view the logs.")

	def run(self, files_dir, date):
		log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
		#  Let's begin!
		# Create db connection
		con = db_init(self.conf.db_dir, self.conf.db_schema)
		# try:
		# Baseline first 30 files
		n = 30  # Step at which the window is moved
		start = 0
		end = n
		# Get a list of the files from the directory that matches the date yesterday (again, update list)
		flist_dir = [x for x in os.listdir(files_dir) if re.match(date, x)]
		if end < len(flist_dir) + 1:  # Base line + 1
			spikes = 0
			while end < len(flist_dir) - 1:  # Needs testing here
				for x in range(start, end):
					print "processing file : {}".format(x)
					with open(files_dir + flist_dir[x], 'r') as f:
						sumcpun = np.array(sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)]))
						summemn = np.array(sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)]))
						print "sumcpun : {}".format(len(sumcpun))
						print "summemn : {}".format(len(summemn))
				meancpu = np.mean(sumcpun)
				meanmem = np.mean(summemn)
				stddcpu = np.std(sumcpun)
				stddmem = np.std(summemn)
				# Get next file (end + 1)
				with open(files_dir + flist_dir[end + 1], 'r') as f:
					print "processing file (n + 1): {}".format(flist_dir[end + 1])
					sumcpunn = sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)])
					summemnn = sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)])
				zscorecpu = (sumcpunn - meancpu) / stddcpu
				zscoremem = (summemnn - meanmem) / stddmem
				if (abs(zscorecpu) > 2.5) and (abs(zscoremem) > 2.5):
					spikes += 1
				#  Shift window by 1
				start += 1
				end += 1
			events = len([x for x in open(files_dir + date.replace('-', '') + '.export.CSV') if (re.search("Netherlands", x))])
			# Store the results
			with con.cursor() as cur:
				cur.execute('INSERT INTO Results(date, spikeNum, eventNum) VALUES(?,?,?)', (date_sep, spikes, events))
			con.commit()
		else:
			log.warning('Error: Not enough files to process date: {}'.format(date_pln))
		con.close()
		# except Exception as e:
		# 	log.warning('Error: {} file: {}'.format(e, x))
		# log.info('Processing finished.')
