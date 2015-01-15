#  @Author Warosaurus

# ZScore example:
# Source: http://www.wikihow.com/Calculate-Z-Scores

import os
import re
import sqlite3 as sql
import logging as log
import numpy as np
import tarfile
import zipfile


# Create a database connection and reutrn it
def _db_init(dir_dbs, dbs_schema):
	con = sql.connect(dir_dbs)
	con.cursor().executescript(open(dbs_schema, "r").read())  # Pass sql file, execute and commit
	return con  # Return connection object


def _extract(dir_arc, dir_tmp, date, fl_t):
	if fl_t == ".tgz":
		with tarfile.open(dir_arc + date + ".tgz", "r") as tar:
			tar.extractall(dir_tmp)
	elif fl_t == ".zip":
		with zipfile.ZipFile(dir_arc + date.replace('-', '') + ".export.CSV.zip", "r") as zf:
			zf.extractall(dir_tmp)


def _clean_tmp(dir_tmp):
	flist = os.listdir(dir_tmp)
	for x in flist:
		try:
			os.remove(dir_tmp + x)
		except Exception as e:
			log.warning("Error: {}".format(e))


def _process(dir_arc, dir_tmp, dir_dbs, dbs_schema, date):
	log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
	# If the database directory does not exist, create it.
	if not os.path.exists(dir_dbs):
		os.makedirs(dir_dbs)
	if not os.path.exists(dir_tmp):
		os.makedirs(dir_tmp)
	#  Let's begin!
	_extract(dir_arc, dir_tmp, date, ".tgz")
	# Create db connection
	con = _db_init(dir_dbs, dbs_schema)
	cur = con.cursor()
	try:
		n = 30  # Step at which the window is moved
		start = 0
		end = n
		# Get a list of the files from the directory that matches the date
		files_lst = [x for x in os.listdir(dir_tmp) if re.match(date, x)]
		files_lst.sort()
		if end < len(files_lst) + 1:  # Base line + 1
			log.info("Processing date: {}".format(date))
			spikes = 0
			mem_lst = []
			# Build the base line
			for x in range(start, end):
				with open(dir_tmp + files_lst[x], 'r') as f:  # With implies close on file object after with block
					mem_lst.append(sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)]))
			while end < len(files_lst) - 1:
				# Calculate the mean of the list of sums
				mem_mean = np.mean(mem_lst)
				# Calculate the standard deviation of the list of sums
				mem_std = np.std(mem_lst)
				# Get the values for the next file (end + 1)
				with open(dir_tmp + files_lst[end + 1], 'r') as f:
					mem_next = sum([int(l.split('= ')[1].split(' ')[0]) for l in f if re.match("HOST-RESOURCES-MIB::hrSWRunPerfMem", l)])
				# Calculate the z-score
				mem_zscore = (mem_next - mem_mean) / mem_std
				if abs(mem_zscore) > 2.5:
					spikes += 1
				# Shift window by 1
				# Thanks to Vera for pointing this out
				mem_lst = mem_lst[1:]
				mem_lst.append(mem_next)
				start += 1
				end += 1
			_extract(dir_arc, dir_tmp, date, ".zip")
			events = len([x for x in open(dir_tmp + date.replace('-', '') + '.export.CSV') if (re.search("Netherlands", x))])
			# # Store the results
			cur.execute('INSERT INTO Results(date, spikes, events) VALUES(?,?,?)', (date, spikes, events))
			con.commit()
		else:
			log.warning('Error: Not enough files to process date: {}'.format(date))
		con.close()
		log.info("Cleaning up after processing date: {}".format(date))
		# Clear the tmp directory
		_clean_tmp(dir_tmp)
	except Exception as e:
		log.warning('Error: {} file: {}'.format(e, x))
	log.info('Processing finished.')


class Process:
	def __init__(self, conf, date):
		_process(conf.dir_arc, conf.dir_tmp, conf.dir_dbs, conf.dbs_schema, date)

