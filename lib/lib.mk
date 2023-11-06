lib/libsqlite3.so:
	@echo "\n[+] Building libsqlite3 for linux"
	@scripts/compile-libsqlite-linux.sh

lib/libsqlite3.0.dylib:
	@echo "\n[+] Building libsqlite3 for macos"
	@scripts/compile-libsqlite-macos.sh