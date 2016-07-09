#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Yogeshwaran
# Search result confidence calculator
# A python script that extracts and writes search engine results to a file

import os
import io
import sys
from optparse import OptionParser
import os.path
import unittest, time, re
import codecs
from sys import argv
import csv
import time
import argparse
import traceback
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.common.proxy import *

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

def google_search(search_word):
	try:
        wd[k].get("https://www.google.com/ncr") #open google [No Country Redirect]
		search_word=search_word.decode('utf-8')
		inputElement = wd[k].find_element_by_name('q').clear()
		inputElement = wd[k].find_element_by_name('q')
        inputElement.send_keys(search_word) #type search key in the search bar
		inputElement.submit()
		time.sleep(5)

		#disecting input into company name, company type and normalizing spaces
		search_word=search_word.encode('utf-8')
		search_word=search_word.strip()
		search_word_original=search_word.strip()

		print search_word,search_word_normal

		searchresults_file = io.open("searchresults", 'a', encoding='utf8') #opening file to store search results

		#fetching top 10 search results
		search_results=[]
		for i in range(1,11):
			result=wd[k].find_element_by_xpath("//a[not((//div[contains(@class,'s')]//div[contains(@class,'kv')]//cite[not(%s)])[%s])]|((//div[contains(@class,'s')]//div[contains(@class,'kv')]//cite[not(%s)])[%s])"%(reject_url,i,reject_url,i))
			search_results.append(result.text)

		#fetching titles of the search results
		search_results_title=[]
		for i in range(1,11):
			result=wd[k].find_element_by_xpath("//a[not((//div[contains(@class,'s')]//div[contains(@class,'kv')]//cite[not(%s)])[%s])]|((//div[contains(@class,'s')]//div[contains(@class,'kv')]//cite[not(%s)])[%s])/preceding::a[1]"%(reject_url,i,reject_url,i))
			search_results_title.append(result.text)

		#fetching descriptions of the search results
		search_results_desc=[]
		for i in range(1,11):
			result=wd[k].find_element_by_xpath("//a[not((//div[contains(@class,'s')]//div[contains(@class,'kv')]//cite[not(%s)])[%s])]|((//div[contains(@class,'s')]//div[contains(@class,'kv')]//cite[not(%s)])[%s])/following::span[contains(@class,'st')][1]"%(reject_url,i,reject_url,i))
			search_results_desc.append(result.text)

		#normalizing titles 
		search_results_title_normal=[]
		for st in search_results_title:
			st=re.sub('[^A-Za-zA-Za-z0-9]+', '',st)
			if st=='':
			    st=' '
			search_results_title_normal.append(st)

		#normalizing search results by replacing the characters like www and .com
		search_results_normal=[]
		for sr in search_results:
			sr=re.sub('(\-)?(\xc2\xad)?(\xe2)?(http://)?(https://)?(www\.)?(en\.)?(in\.)?(\.com\.au)?(\.com\.br)?(\.co\.za)?(\.co\.nz)?(\.com\.tr)?(\.com\.fr)?(\.uk\.com)?(\.ie)?(\.sc)?(\.at)?(\.eu)?(\.ch)?(\.us)?(\.fi)?(\.sg)?(\.co.uk)?(\.ca)?(\.co.in)?(\.co.jp)?(\.com\.br)?(\.edu)?(\.int)?(\.es)?(\.de)?(\.co\.fr)?(\.org\.uk)?(\.net)?(\.be)?(\.ee)?(\.it)?(\.vc)?(\-)?(\.com)?(\.co)?(\.fr)?(\.io)?(\.ph)?(\.info)?(\.in)?(\.tv)?(\.org)?(\.dk)?(\.biz)?','',sr.rstrip())
			sr=re.sub('(/.*)','',sr.rstrip())
			if sr=='':
			    sr=' '
			search_results_normal.append(sr)
		searchresults_file.write(search_word_original.decode('utf-8') + "^" + search_results[0] + "^" + search_results_title[0] + "^" + search_results_desc[0] + "^" + search_results[1] + "^" + search_results_title[1] + "^" + search_results_desc[1] + "^" + search_results[2] + "^" + search_results_title[2] + "^" + search_results_desc[2] + "^" + search_results[3] + "^" + search_results_title[3] + "^" + search_results_desc[3] + "^" + search_results[4] + "^" + search_results_title[4] + "^" + search_results_desc[4] + "^" + search_results[5] + "^" + search_results_title[5] + "^" + search_results_desc[5] + "^" + search_results[6] + "^" + search_results_title[6] + "^" + search_results_desc[6] + "^" + search_results[7] + "^" + search_results_title[7] + "^" + search_results_desc[7] + "^" + search_results[8] + "^" + search_results_title[8] + "^" + search_results_desc[8] + "^" + search_results[9] + "^" + search_results_title[9] + "^" + search_results_desc[9] + "\n");
		print search_word,search_word_normal,search_results,search_results_title,search_results_desc,search_results_title_normal,search_results_normal
	except Exception:
		print traceback.format_exc()
		print 'Exception occured while doing google search'
	return search_word_original,search_word,search_word_normal,search_results,search_results_title,search_results_desc,search_results_title_normal,search_results_normal

searchresults_file = "/tmp/searchitems.txt"
file_open = open(searchresults_file)
wd=['','']
k=1

with file_open as fp:
	for search_word in fp:
		initialize_webdriver(k)
		try:
			search_word_original,search_word,search_word_normal,search_results,search_results_title,search_results_desc,search_results_title_normal,search_results_normal = google_search(search_word)
			wd[k].quit()
		except Exception:
			print traceback.format_exc()
			print 'Unexpected Exception'
			kill_browser()
			wd[k].quit()
