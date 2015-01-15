#!/usr/bin/env python
# @Author Warosaurus

import datetime as dt
from config import Config
from core import Process, Fetch

if __name__ == "__main__":
	# Time period
	date_s = dt.date(2014, 12, 11)
	date_e = dt.date(2015, 01, 05)  # Last I checked there were no more files after this day.
	# Get the days between the start and the end of the time period
	days = [str((date_s + dt.timedelta(days=x))) for x in range((date_e - date_s).days + 1)]
	c = Config()
	for day in days:
		Fetch(c, day)
		Process(c, day)