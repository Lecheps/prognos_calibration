#!/bin/bash
echo $PWD
ls -lah /
ls -lah /workspace
cd /root/gotm/fabm-prognos 
mkdir build
cd build
cmake ../src -DFABM_HOST=gotm
make
ls
cd /root/gotm/code
mkdir build
cd build
cmake ../src -DFABM_BASE=/root/gotm/fabm-prognos
make
cp /root/gotm/code/build/gotm /root/gotm/gotm
/root/gotm/gotm

