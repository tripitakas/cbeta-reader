#!/bin/sh
# Run it in the project path to download meta files.

if [ ! -d data/meta ] ; then
    curl -o meta.zip https://codeload.github.com/tripitakas/cbeta-reader/zip/meta
    unzip -d data meta.zip
    mv data/cbeta-reader-meta data/meta
    rm meta.zip
fi
