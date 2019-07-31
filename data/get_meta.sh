#!/bin/sh
# Run it in the project path to download meta files.

if [ ! -d data/meta/juan ] ; then
    tar zxvf data/meta/juan.tgz -C data/meta
fi
if [ ! -d data/meta/mulu ] ; then
    tar zxvf data/meta/mulu.tgz -C data/meta
fi
if [ ! -d data/xml/ori ] ; then
    mkdir data/xml
    tar zxvf tests/xml/ori.tgz -C data/xml
fi