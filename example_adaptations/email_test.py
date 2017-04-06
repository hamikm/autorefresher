import smtplib
import urllib2
import time
import re
import pytz
from HTMLParser import HTMLParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from dateutil.parser import parse
from datetime import datetime
from bs4 import BeautifulSoup

def sendEmail(recipients, new_discussion_html_str):
	fromaddr = "scripthamikmukelyan@gmail.com"
	toaddr = recipients
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['Subject'] = "Testing"
	 
	msg.attach(MIMEText(new_discussion_html_str, 'html'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "rootpass")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def getHTMLFromPage(url):
	import urllib2
	response = urllib2.urlopen(url)
	return response.read()

def getDiscussionTextFromRawHTML(hanford_discussion_raw_html):
	parsedDoc = BeautifulSoup(hanford_discussion_raw_html, 'html.parser')
	return parsedDoc.find('pre', { 'class' : 'glossaryProduct' }).prettify()

def getRawDateFromHTML(html):
	pattern = re.compile('\d{3,4} (PM|AM) (PDT|PST)')
	splitted = html.split('\n')
	for elem in splitted:
		m = pattern.match(elem)
		if m:
			return elem # m.group(0)
	return None

def datetimeFromRawDate(raw_date):
	arr = raw_date.split()
	time_part = arr[0]
	if len(time_part) == 3:
		time_part = time_part[:1] + ":" + time_part[1:]
	elif len(time_part) == 4:
		time_part = time_part[:2] + ":" + time_part[2:]
	arr[0] = time_part
	new_date = ' '.join(arr)
	return parse(new_date)

if __name__ == '__main__':
	utc = pytz.timezone("UTC")
	last_date = datetime.now().replace(tzinfo=utc)
	while True:
		hanford_discussion_url = 'http://forecast.weather.gov/product.php?site=HNX&issuedby=HNX&product=AFD&format=CI&version=1&glossary=1'
		hanford_discussion_raw_html = getHTMLFromPage(hanford_discussion_url)
		discussion_text = getDiscussionTextFromRawHTML(hanford_discussion_raw_html)
		update_time = datetimeFromRawDate(getRawDateFromHTML(discussion_text)).replace(tzinfo=utc)
		if update_time > last_date:
			html_email = '<html><head></head><body>' + discussion_text + '</body></html>'
			sendEmail(['hamikmukelyan@gmail.com', 'gdrayna@gmail.com', 'ksilsbee@gmail.com'], html_email)
			last_date = update_time
		time.sleep(60 * 10) # sleep for 10 mins
