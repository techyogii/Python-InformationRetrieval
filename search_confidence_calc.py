#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Yogeshwaran
# Search result confidence calculator
# This Python script calculates the confidence score of a search result based on the string match accuracy between the search keyword and the search results
# The list of normalized search results obtained from the google_search.py file can be used as an input for this script

import os
import os.path
import difflib
import codecs
import io
import sys
from sys import argv
import csv
import time
import argparse
import traceback

def confidence_calc(search_results_normal): #this function is used to calculate confidence score of the search results

	confidencescore_file = "/tmp/searchresults_confidence.txt"
	file_open = io.open(confidencescore_file, 'a', encoding='utf8')

	v1 = []
	v2 = []
	v3 = []

	for search_result in search_results_normal: 
	        v1.append(difflib.SequenceMatcher(None,search_word,(search_result[0:len(search_word)]).encode('utf-8')).ratio())
	        v2.append(difflib.SequenceMatcher(None,search_word[0:len(search_result)],search_result.encode('utf-8')).ratio())

	for search_result_title in search_results_title_normal:
		if company_type:
			v3.append(difflib.SequenceMatcher(None,search_word_normal,(search_result_title[0:len(search_word_normal)]).encode('utf-8')).ratio())
		else:
			v3.append(0)
	
	v1_scores=[float(x) for x in v1]
	v1_scores.sort(reverse=True)
	v2_scores=[float(x) for x in v2]
	v2_scores.sort(reverse=True)
	v3_scores=[float(x) for x in v3]
	v3_scores.sort(reverse=True)

	v=[v1[0]+v2[0],v1[1]+v2[1],v1[2]+v2[2],v1[3]+v2[3],v1[4]+v2[4],v1[5]+v2[5],v1[6]+v2[6],v1[7]+v2[7],v1[8]+v2[8],v1[9]+v2[9]]
	v_scores=[v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9]]
	v_scores=[float(x) for x in v_scores]
	v_scores.sort(reverse=True)

	best_scores=[v_scores[0],v_scores[1],v_scores[2],v_scores[3],v_scores[4],v_scores[5],v_scores[6],v_scores[7],v_scores[8],v_scores[9]]

	best_results=[]
	for best_score in best_scores:
	    if best_score == v[0]:
	        best_result = search_results[0]
	    elif best_score == v[1]:
	        best_result = search_results[1]
	    elif best_score == v[2]:
	        best_result = search_results[2]
	    elif best_score == v[3]:
	        best_result = search_results[3]
	    elif best_score == v[4]:
	        best_result = search_results[4]
	    elif best_score == v[5]:
	        best_result = search_results[5]
	    elif best_score == v[6]:
	        best_result = search_results[6]
	    elif best_score == v[7]:
	        best_result = search_results[7]
	    elif best_score == v[8]:
	        best_result = search_results[8]
	    elif best_score == v[9]:
	        best_result = search_results[9]
	    else:
	        best_result = "None"
	            
	    best_results.append(best_result)

	#segregating search results based on high, medium and low confidence scores
	best_result_conf=['','','','','','','','','','']
	for i in range(0,10):
	        if best_scores[i] == 2:    
	                best_result_conf[i]='High'
	        elif (v1_scores[i] == 1 or v2_scores[i] == 1) and (v3_scores[i]>0.80):
	                best_result_conf[i]='High'
	        elif v1_scores[i] == 1 or v2_scores[i] == 1:
	                best_result_conf[i]='Medium'
	        else: best_result_conf[i]='Low'

	#writing to file
	confidencescore_file.write(search_word_original.decode('utf-8') + "^" + best_results[0] + "^" + best_result_conf[0] + "^" + best_results[1] + "^" + best_result_conf[1] + "^" + best_results[2] + "^" + best_result_conf[2] + "^" + search_results[0] + "^" + search_results[1] + "^" + search_results[2] + "^" + search_results[3] + "^" + search_results[4] + "^" + search_results[5] + "^" + search_results[6] + "^" + search_results[7] + "^" + search_results[8] + "^" + search_results[9] + "\n");
	print best_results,best_result_conf


best_results,best_result_conf = confidence_calc()
