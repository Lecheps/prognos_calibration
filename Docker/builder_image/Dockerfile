FROM debian:latest
RUN apt-get -qq update > /dev/null && apt-get install -qqy \
    cmake \
    make \
    gcc \
    gfortran \  
    libnetcdf-dev \
    libnetcdff-dev \
    netcdf-bin > /dev/null \
    && rm -rf /var/lib/apt/lists/*
