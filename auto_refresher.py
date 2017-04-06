import smtplib
import urllib2
import time
from HTMLParser import HTMLParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from dateutil.parser import parse
from datetime import datetime
from bs4 import BeautifulSoup

old_part_of_interest = ''

def sendEmail(recipients, new_content_html):
	fromaddr = TODO # string
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['Subject'] = TODO # string
	 
	msg.attach(MIMEText(new_content_html, 'html'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	password = TODO # string
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, recipients, text)
	server.quit()

def getHTMLFromPage(url):
	import urllib2
	response = urllib2.urlopen(url)
	return response.read()

def getPartOfInterestFromRawHTML(raw_html):
	parsedDoc = BeautifulSoup(raw_html, 'html.parser')
	lookForThisTag = TODO # e.g. 'pre'
	strStrDictOfAttrbs = TODO # e.g.  { 'class' : 'glossaryProduct' }
	return parsedDoc.find(lookForThisTag, strStrDictOfAttrbs).prettify()

if __name__ == '__main__':
	while True:
		theUrl = TODO # e.g. 'http://forecast.weather.gov/product.php?site=HNX&issuedby=HNX&product=AFD&format=CI&version=1&glossary=1'
		raw_html = getHTMLFromPage(theUrl)
		part_of_interest = getPartOfInterestFromRawHTML(raw_html)
		if part_of_interest != old_part_of_interest:
			html_email = '<html><head></head><body>' + part_of_interest + '</body></html>'
			lstOfRecipients = TODO # list of email addresses as strings
			sendEmail(lstOfRecipients, html_email)
			old_part_of_interest = part_of_interest
		sleepTimeMins = TODO # int
		time.sleep(60 * sleepTimeMins)

