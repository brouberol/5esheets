#!/usr/bin/env bash

apt-get install -y build-essential wget tcl

# link associated with sqlite 3.42.0, found on https://www.sqlite.org/src/timeline?t=version-3.42.0 -> https://www.sqlite.org/src/info/831d0fb2836b71c9
wget https://www.sqlite.org/src/tarball/831d0fb2/SQLite-831d0fb2.tar.gz
tar -xzvf SQLite-831d0fb2.tar.gz
cd SQLite-831d0fb2

CPPFLAGS="-DSQLITE_ENABLE_FTS5" ./configure
make
cp .libs/libsqlite3.so ./..
