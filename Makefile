script.zip: config.txt script.py
	zip -j script.zip config.txt script.py

clean:
	$(RM) script.zip
