# Option_Scraper
Python 3: Requires pandas, statistics, twilio, bs4, matplotlib, lxml

I removed all my personal twilio info, but it's easy to sign up for an account and put that info in the send_message function 
in mainfile.py. Or just change send_message(alertstring) to pass or something like that. 

run mainfile.py to pull data, perform calculations, plot vol series and implied vol, create excel summary sheet of risk characteristics,
and send alert message. Change expiration and security in lines 11 and 12

Note: The code is pretty hacky/crude, and even worse - it's at the mercy of yahoo who changes their site a lot and sometimes
this breaks everything or just gives ridiculous theos (this is especially true for illiquid options or whenever yahoo decides
not to frequently update their tables). But generally this project is good for getting ballpark theoreticals, risk characteristics, and vol
