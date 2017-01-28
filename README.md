# SiteCheck
Configuration:
SiteCheck links to import.io API's to quickly inform you if changes have been made to a particular data set, in most cases, the contents of a website such as forum posts / job listings etc.

SiteCheck is designed to work with Python 2.7.8 and is not tested with older or newer versions at this time.

1) Create an import.io account then download and install the desktop app.

2) Using "API from URL 2.0", create extractors for websites that you want to watch for updates. Import.io has tutorials on how to create extractors (very easy). A new extractor will be needed for each website that you want to watch (ie: watching 5 sites will require 5 extractors).

3) After publishing each extractor, you will need to get it's API number:
	Select the Extractor on the left column of the import.io app.
	Click "GET API"
	You will see a string of text similar to this:
		https://api.import.io/store/data/b6eh4176-1d8d-4242-b8fd-9e6951034252/_query?input/webpage/url=http%3A%2F%2Fwww.peopleperhour.com%2Ffreelance-writing-jobs&_user=0f764215-d305-470b-993e-b6a7b596f686&_apikey=
		
	The API number is the number after /data/ and before /_query?, in this case it would be: b6eh4176-1d8d-4242-b8fd-9e6951034252
	
4) Open sitelist.txt and add the website nick-name, API number and URL for each site.
	FORMATTING IS IMPORTANT: deviation from the predefined format will cause the software to hang. sitelist.txt should be formatted as follows:
			Site1
			API Number
			Website URL
			
			Site2
			API Number for Site2
			Website URL for Site2
			
			etc.....

5) After configuring websites to watch, open emailconfig.txt and input your email information, again following the formatting within the template.

6) Launch SiteCheckUI, click Start Scraper and wait for emails.
