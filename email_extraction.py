#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Yogeshwaran
# This python script recursively crawls a list of websites and pull out the contact emails address for each one of them

import os
import os.path
import difflib
import unittest, time, re
import codecs
import io
import random
from urlparse import urlparse
import sys
from sys import argv
import csv
import time
import argparse
import traceback
from threading import Timer
from timeout import timeout
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.common.proxy import *

@timeout(300)	
def email_extraction(url):
	url=url.strip()
	#open file containing list of URLs
	email_extraction_output = io.open("/tmp/website_emails.txt", 'ab+')
	try:
		#check if url contains any protocol
		http = re.search('http|https',url)
		if http:   
			wd[k].get(url)
		else:
			wd[k].get('http://'+url)
		time.sleep(5)
		#download html source of the home page
		html_source = wd[k].page_source
		html_source = html_source.encode('utf-8')
		#fetching all emails present in the html page
		emails=[]
		for email in get_emails(html_source):
			emails.append(email)

		#extracting list of links that could potentially lead to a page containing contact details
		contact_links=wd[k].find_elements_by_xpath("(%s)"%(contact_link_xpath))
		num_links=len(contact_links)

		if (num_links > 0):
			#browsing each of the contact link and performing the same action of extracing the emails as we performed in the home page
			for i in range(1,num_links+1):
				WebDriverWait(wd[k], 120).until(EC.element_to_be_clickable((By.XPATH,contact_link_xpath)))
				time.sleep(5)
				try:
					wd[k].find_element_by_xpath("(%s)[%s]"%(contact_link_xpath,i)).click()
				except Exception:
					print ''
				time.sleep(5)
				html_source = wd[k].page_source
				html_source = html_source.encode('utf-8')
				for email in get_emails(html_source):
					email = re.sub('[0-9][0-9][0-9].[0-9][0-9][0-9].[0-9][0-9][0-9][0-9]','',email)
					emails.append(email)
				emails = list(set(emails))
				if http:
					wd[k].get(url)
				else:
					wd[k].get('http://'+url)
	except Exception:
		print traceback.format_exc()
		emails=[]
	emails = list(set(emails))
	emails = [s for s in emails if not email_reject_regex.match(s)]
	print url.decode('utf-8') + "^" + '^'.join(emails)
	email_extraction_output.write(url.decode('utf-8') + "^" + ','.join(emails) +"^"+"\n");

def get_emails(s):
    return (email[0] for email in re.findall(email_regex, s) if not email[0].startswith('//'))

def kill_browser():
	time.sleep(100)
	os.system("killall -9 firefox")

def initialize_webdriver(k):
	#Selenium Wedriver
	if(k==0):
		wd[k]=WebDriver()
		wd[k].set_window_size(1124, 850)
	#PhantomJS - Headless web browser
	elif(k==1):
#		service_args1 = ['--load-images=false',]
		wd[k] = webdriver.PhantomJS('phantomjs',service_log_path='/tmp/ghostdriver.log')
		wd[k].set_window_size(1124, 850)
	wd[k].implicitly_wait(15)
	wd[k].set_page_load_timeout(60)
	return wd[k]

wd=['','']
k=1

#URL patterns that are most likely to contain contact information
contact_link_xpath="//a[contains(@href,'policy') or contains(@href,'kontakt') or contains(@href,'contact') or contains(@href,'email') or contains(.,'Kontakt') or contains(.,'KONTAKT') or contains(.,'kontakt') or contains(.,'contact') or contains(.,'CONTACT') or contains(.,'Contact') or contains(.,'Gallery') or contains(.,'GALLERY') or .='ABOUT' or .='about' or .='About' or .='ABOUT US' or .='About Us' or .='about us' or .='Privacy Policy' or .='PRIVACY POLICY' or .='POLICY' or .='Policy' or .='policy' or .='privacy policy' or .='Privacy Statement' or .='CONTATTI' or .='Contatti' or .='contatti' or .='CONTATTO' or .='contatto' or .='Contatto' or .='terms of use' or .='TERMS OF USE' or .='Terms Of Use' or .='Nous contacter' or .='Privacy' or .='privacy' or .='PRIVACY' or .='Wholesale Enquiries' or .='Terms and Conditions' or contains(.,'Imprint') or contains(.,'Impressum') or contains(.,'IMPRINT') or contains(.,'IMPRESSUM') or contains(.,'imprint') or contains(.,'impressum') or contains(.,'CONDITIONS') or contains(.,'Conditions') or contains(.,'conditions') or .='Returns' or .='T & Cs' or contains(.,'Terms & conditions') or contains(.,'Legal') or contains(.,'LEGAL') or contains(.,'legal')][not(//a[contains(@href,'mailto') or contains(@href,'Mailto')]//text()[contains(.,'@')] or //text()[contains(.,'@') and contains(.,'.co') and not(contains(.,'{') or contains(.,'import') or contains(.,'Import') or contains(.,'CDATA') or contains(.,'document.write'))] or //text()[contains(.,'@') and contains(.,'.de')] or normalize-space(substring-after(//a[contains(@href,'mailto:') or contains(@href,'Mailto:')]/@href,'ailto:')))]"

#Regex that will be used to extract email addresses from the HTML content
email_regex = re.compile(("([A-Za-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@)(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(\.|"
                    "\sdot\s))+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)"))

#Email address patterns that should not be considered as they cannot be used for contacting purpose
email_reject_regex = re.compile(r'.*(png|jpg|images|img|you|emailaddress|yourname|myname|example|webmaster|dontreply|donotreply|wp-content|logo|ajax|webmaster|privacy|careers|copyright|press|mediaenquiries|terms|media|publicrelations|return|editor).*')

num_lines = sum(1 for line in open("/tmp/url_list.txt"))
file_open = open("/tmp/url_list.txt")
with file_open as fp:
	for url in fp:
		initialize_webdriver(k)
		try:
			email_extraction(url)
			wd[k].quit()
		except Exception:
			print traceback.format_exc()
			print 'Unexpected Exception'
			kill_browser()
			wd[k].quit()
