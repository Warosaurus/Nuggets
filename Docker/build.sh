#!/bin/bash
#@Author Warosaurus
#This file will build all the necessary images to create the containers for the infrastructure.

cd ubuntuLocal
./ubuntulocal.sh
cd ../ubuntuPython
./ubuntuPython.sh
cd ../ubuntuSQLite
./ubuntuSQLite.sh
