#!/usr/bin/env python
import os
from ftplib import FTP
import config
import tarfile
import datetime as dt
# Run this only once. it's very dumb.


def justdownload():
    c = config.Config()
    ftp = FTP(c.ftp_ip)
    ftp.login(c.ftp_username, c.ftp_password)
    ftp.cwd("datatransport/host01/")
    file_dir = c.files_dir
    date_s = dt.date(2014, 12, 11)
    date_e = dt.date(2015, 01, 05)
    days = [str((date_s + dt.timedelta(days=x))) for x in range((date_e - date_s).days + 1)]
    flist_ftp = ftp.nlst()[2:]
    day_arc = [day for day in days if (day + ".tgz" in flist_ftp)]
    # Exclude the archived files
    day_nor = [day for day in days if (day not in day_arc)]
    # for day in day_arc:
    #     print "Downloading : {}".format(day + '.tgz')
    #     # Download archive
    #     with open(file_dir + day + '.tgz', "w+") as f:  # With implies close after scope
    #         ftp.retrbinary('RETR %s' % day + '.tgz', f.write)
    for day in day_nor:
        flist = [x for x in ftp.nlst()[2:] if (x[:len(day)] == day)]
        with tarfile.open(file_dir + day + ".tgz", "w:tgz") as tar:
            for fl in flist:
                print "downloading file : {}".format(fl)  # Testing
                with open(file_dir + fl, "w+") as f:  # With implies close after scope
                    ftp.retrbinary('RETR %s' % fl, f.write)
                tar.add(fl, file_dir + fl)
                os.remove(file_dir + fl)
    ftp.quit()

if __name__ == "__main__":
    justdownload()