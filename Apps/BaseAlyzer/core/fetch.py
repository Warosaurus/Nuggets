import os
import tarfile
from ftplib import FTP


# Create a ftp connection and reutrn it
def ftp_init(files_dir, ftp_ip, ftp_username, ftp_password):
	ftp = FTP(ftp_ip)
	ftp.login(ftp_username, ftp_password)
	return ftp


class Fetch:
	def __init__(self, date, files_dir, ftp_settings):
		self.download(date, files_dir, ftp_settings)

	def download(self, date, files_dir, ftp_settings):
		ftp = ftp_init(files_dir, ftp_settings[0], ftp_settings[1], ftp_settings[2])
		ftp.cwd("datatransport/host01/")
		flist = ftp.nlst()[2:]
		flist_dir = []
		# Has the date been archived
		if (date + '.tgz') in flist:
			print "Downloading : {}".format(date + '.tgz')
			# Download archive
			with open(files_dir + date + '.tgz', "w+") as f:  # With implies close after scope
				ftp.retrbinary('RETR %s' % date + '.tgz', f.write)
			# Extract archive
			with tarfile.open(files_dir + date + '.tgz') as tf:
				tf.extractall(files_dir)
		else:
			flist = [x for x in ftp.nlst()[2:] if (x[:len(date)] == date)]
			for fl in flist:
				print "downloading file : {}".format(fl)  # Testing
				with open(files_dir + fl, "w+") as f:  # With implies close after scope
					ftp.retrbinary('RETR %s' % file, f.write)
		ftp.quit()

		# 		# Get a list of all the files from the ftp that matches the date yesterday
		# flist = [x for x in ftp.nlst()[2:] if re.search(date_sep, x)]
		# # Get a list of the files from the directory that matches the date yesterday
		# flist_dir = [x for x in os.listdir(files_dir) if re.search(date_sep, x)]
		# # Exclude files that have already been downloaded for that date
		# flist_ftp = [x for x in flist if (x not in flist_dir)]

		# # Deal with events information
		# res = url.urlopen('http://data.gdeltproject.org/events/index.html').read().split('<LI>')[4:]
		# fil = [x for x in res if (date_pln in x)][0].split('>')[1].split('<')[0]
		# # Download events file
		# dwnlod = url.urlopen('http://data.gdeltproject.org/events/' + fil)
		# with open(files_dir + fil, 'w+') as f:
		# 	f.write(dwnlod.read())
		# with z.ZipFile(files_dir + fil) as zf:
		# 	zf.extractall(files_dir)
		# os.remove(files_dir + fil)
