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
def _db_init(db_location, db_schema):
	con = sql.connect(db_location)
	con.cursor().executescript(open(db_schema, "r").read())  # Pass sql file, execute and commit
	return con  # Return connection object

class Process:
	def __init__(self, conf, date):
		self.conf = conf
		self.run(self.conf.files_dir, date)

	def run(self, files_dir, date):
		log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
		#  Let's begin!
		# Create db connection
		con = _db_init(self.conf.db_dir, self.conf.db_schema)
		# try:
		# Baseline first 30 files
		n = 30  # Step at which the window is moved
		start = 0
		end = n
		# Get a list of the files from the directory that matches the date and is not a archive
		flist_dir = [x for x in os.listdir(files_dir) if x[:len(date)] == date and (x[-4:] is not ".tgz")]
		flist_dir.sort()
		if end < len(flist_dir) + 1:  # Base line + 1
			spikes = 0
			while end < len(flist_dir) - 1:  # Needs testing here
				sumcpun = []
				summemn = []
				for x in range(start, end):
					with open(files_dir + flist_dir[x], 'r') as f:
						sumcpun.append(sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)]))
						f.seek(0)
						summemn.append(sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)]))
				meancpu = np.mean(sumcpun)
				meanmem = np.mean(summemn)
				stddcpu = np.std(sumcpun)
				stddmem = np.std(summemn)
				# Get next file (end + 1)
				with open(files_dir + flist_dir[end + 1], 'r') as f:
					sumcpunn = sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfCPU", l)])
					f.seek(0)
					summemnn = sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)])
				zscorecpu = (sumcpunn - meancpu) / stddcpu
				zscoremem = (summemnn - meanmem) / stddmem
				print "zscorecpu : %.2f" % zscorecpu
				print "zscoremem : %.2f" % zscoremem
				if (abs(zscorecpu) > 2.5) and (abs(zscoremem) > 2.5):
					spikes += 1
				#  Shift window by 1
				start += 1
				end += 1
				print "spikes : {}".format(spikes)
			# events = len([x for x in open(files_dir + date.replace('-', '') + '.export.CSV') if (re.search("Netherlands", x))])
			# # Store the results
			# with con.cursor() as cur:
			# 	cur.execute('INSERT INTO Results(date, spikeNum, eventNum) VALUES(?,?,?)', (date, spikes, events))
			# con.commit()
		else:
			log.warning('Error: Not enough files to process date: {}'.format(date))
		con.close()
		# except Exception as e:
		# 	log.warning('Error: {} file: {}'.format(e, x))
		# log.info('Processing finished.')
