#!/bin/bash
cd /root/gotm
cp ./code/build/gotm gotm
cp /usr/lib/x86_64-linux-gnu/libnetcdff.so.6.1.1 libnetcdff.so.6
cp /usr/lib/x86_64-linux-gnu/libnetcdf.so.11.4.0 libnetcdf.so.11
cp /usr/lib/x86_64-linux-gnu/libgfortran.so.3.0.0 libgfortran.so.3
tar -cf gotm.tar gotm libnetcdff.so.6 libnetcdf.so.11 libgfortran.so.3
