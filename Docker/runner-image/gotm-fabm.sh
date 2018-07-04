#!/bin/bash
echo $PWD
cd /root/gotm/fabm-prognos 
mkdir build
cd build
cmake ../src -DFABM_HOST=gotm
make
cd /root/gotm/code
mkdir build
cd build
cmake ../src -DFABM_BASE=/root/gotm/fabm-prognos
make
cp /root/gotm/code/build/gotm /usr/bin
