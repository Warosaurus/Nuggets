#!/usr/bin/env python
#@Author Warosaurus

from config import Config
from core import Process

if __name__ == "__main__":
	c = Config()
	p = Process()
	p.run(c)