#!/usr/bin/env bash

# Thanks Simon Willison!
# https://til.simonwillison.net/sqlite/sqlite-version-macos-python#user-content-adding-compiler-options

sqlite_version=3420000

wget https://www.sqlite.org/2023/sqlite-amalgamation-${sqlite_version}.zip
unzip sqlite-amalgamation-${sqlite_version}.zip
pushd sqlite-amalgamation-${sqlite_version}
gcc -dynamiclib sqlite3.c -o libsqlite3.0.dylib -lm -lpthread -DSQLITE_ENABLE_FTS5
popd
mv sqlite-amalgamation-${sqlite_version}/libsqlite3.0.dylib ./lib/
rm -r sqlite-amalgamation-${sqlite_version}.zip sqlite-amalgamation-${sqlite_version}
