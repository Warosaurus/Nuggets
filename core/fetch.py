import os
import re
import tarfile
import shutil
import urllib2
from ftplib import FTP
import logging as log


# Create a ftp connection and reutrn it
def _ftp_init(ftp_i, ftp_u, ftp_p):
	ftp = FTP(ftp_i)
	ftp.login(ftp_u, ftp_p)
	return ftp


# Clean up directory
def _clean(dir_dwl):
	flist = os.listdir(dir_dwl)
	for x in flist:
		try:
			os.remove(dir_dwl + x)
		except Exception as e:
			log.warning("Error: {}".format(e))


def _fetch(dir_dwl, dir_arc, ftp_i, ftp_u, ftp_p, date):
	# Init stuff: Create logs, directories
	log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
	if not os.path.exists(dir_arc):
		os.makedirs(dir_dwl)
	if not os.path.exists(dir_dwl):
		os.makedirs(dir_dwl)
	# Is the date achived locally?
	# No:
	if (date + ".tgz") not in os.listdir(dir_arc):
		ftp = _ftp_init(ftp_i, ftp_u, ftp_p)
		ftp.cwd("datatransport/host01/")
		# Is there an archived version on the ftp?
		# Yes:
		if (date + ".tgz") in ftp.nlst("."):
			# Download the file then once downloaded move it to the archived dir
			log.info("Downloading: {}".format(date + ".tgz"))
			with open(dir_dwl + date + ".tgz", "w+") as f:
				ftp.retrbinary('RETR %s' % date + ".tgz", f.write)
				shutil.move(dir_dwl + date + ".tgz", dir_arc)
		# No:
		# Are the files on the ftp for that day?
		elif len([x for x in ftp.nlst(".") if re.match(date, x)]) > 30:
			# Yes
			fl_lst = [x for x in ftp.nlst(".") if re.match(date, x)]
			# Download those files
			for fl in fl_lst:
				with open(dir_dwl + fl, "w+") as f:  # With implies close after scope
					ftp.retrbinary('RETR %s' % fl, f.write)
			# Write them to and archive
			try:
				log.info("Creating archive: {}".format(dir_arc + date + ".tgz"))
				with tarfile.open(dir_arc + date + ".tgz", "w:gz") as tf:
					for fl in fl_lst:
						tf.add(dir_dwl + fl, fl)
			except Exception as e:
				log.warning("Error: {}".format(e))
		ftp.quit()  # Done with ftp
	# Is the events file archived locally?
	fl_events = date.replace("-", "") + ".export.CSV.zip"
	# No:
	if fl_events not in os.listdir(dir_arc):
		# Get it from the site
		print "Downloading: {}".format(fl_events)
		url_dwl = urllib2.urlopen('http://data.gdeltproject.org/events/' + fl_events)
		with open(dir_arc + fl_events, 'w+') as f:
			f.write(url_dwl.read())
	_clean(dir_dwl)


class Fetch:
	def __init__(self, conf, date):
		_fetch(conf.dir_dwl, conf.dir_arc, conf.ftp_ip, conf.ftp_username, conf.ftp_password, date)
