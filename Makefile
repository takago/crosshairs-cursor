install:
	cp crosshairs_cursor.py /usr/local/bin/crosshairs_cursor
	chmod uog+x /usr/local/bin/crosshairs_cursor

	@echo
	@echo "# sudo apt-get install python3-qtpy"
	@echo "# cp crosshairs_cursor.desktop  ~/.config/autostart/"

uninstall:
	rm /usr/local/bin/crosshairs_cursor
	@echo
	@echo "# rm ~/.config/autostart/crosshairs_cursor.desktop"

