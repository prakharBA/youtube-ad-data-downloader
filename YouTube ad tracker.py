from selenium import webdriver 
import random
import csv
from random import randrange
import time 
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys
from random import choice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from datetime import date
from googleapiclient import discovery
from apiclient  import discovery

import gspread
from oauth2cient.service_account import ServiceAccountCredentials

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client import file,client,tools


#random weights to search term
class WeightedRandomizer:
	def __init__ (self, weights):
		self.__max = .0
		self.__weights = []
		for value, weight in weights.items ():
			self.__max += weight
			self.__weights.append ( (self.__max, value) )
	def random (self):
		r = random.random () * self.__max
		for ceil, value in self.__weights:
			if ceil > r: return value

search_term = ['python selenium','hello world']

#search_term = search_term1+search_term2+search_term3+search_term4

#x cancel

print(search_term)

w = {search_term[0]: 2,search_term[1]: 2,search_term[2]: 2}

wr = WeightedRandomizer(w)

#driver.find_element_by_class_name('style-scope ytd-video-renderer').click()
#search and click
def search_click(wds):
	search_t = wr.random()
	search = wds.find_element_by_css_selector('input[id=search]')
	time.sleep(random.randint(2,3))
	search.clear()
	time.sleep(random.randint(2,5))
	for character in search_t:
		search.send_keys(character)
		time.sleep(0.2)
	time.sleep(random.randint(4,6))
	wds.find_element_by_id("search-icon-legacy").click()
	time.sleep(random.randint(8,10))
	try:
		r=random.randint(0,3)
		wds.find_elements_by_class_name('style-scope ytd-video-renderer')[r].click()
	except:
		home_page_1st_reco(wds)
	

#go to home, click on recommended
def home_page_1st_reco(wds):
	wds.find_element_by_id('logo').click()
	time.sleep(random.randint(9,15))
	try:
		r=random.randint(0,3)
		wds.find_elements_by_id('dismissable')[r].click()
	except:
		search_click(wds)


#video len
def v_len(wds):
	wds.execute_script('document.getElementsByTagName("video")[0].pause()')
	time.sleep(random.randint(2,4))
	video_len = wds.find_element_by_class_name('ytp-time-duration').get_attribute("textContent")
	wds.execute_script('document.getElementsByTagName("video")[0].play()')
	return float(video_len.split(":")[0])*60+float(video_len.split(":")[1])


#play_next
def play_next(wds):
	wds.execute_script('document.getElementsByTagName("video")[0].pause()')
	wds.find_element_by_class_name('ytp-left-controls').find_element_by_class_name('ytp-next-button').click()


#click back
def click_back(wds):
	wds.back()

ads = []



def detect_ad(wds):
	page = wds.page_source
	if "ytp-ad-player-overlay" in page:
		ads.append([])
		try:
			wds.execute_script('document.getElementsByTagName("video")[0].pause()')
			time.sleep(1)
			ads[len(ads)-1].append(wds.find_element_by_class_name('ytp-title-subtext').text)
			ads[len(ads)-1].append(wds.find_element_by_class_name('ytp-title-link').text)
			ads[len(ads)-1].append(wds.find_element_by_class_name('ytp-ad-player-overlay-instream-info').find_element_by_class_name('ytp-ad-button-text').text)
			print(wds.find_element_by_class_name('ytp-title-subtext').text)
			print(wds.find_element_by_class_name('ytp-title-link').text)
			print(wds.find_element_by_class_name('ytp-ad-player-overlay-instream-info').find_element_by_class_name('ytp-ad-button-text').text)
		except:
			try:
				time.sleep(1)
				ads[len(ads)-1].append(wds.find_element_by_id('action-companion-click-target').find_element_by_id('header').text)
				ads[len(ads)-1].append(wds.find_element_by_id('domain').text)
				ads[len(ads)-1].append(wds.find_element_by_class_name('ytp-ad-player-overlay-instream-info').find_element_by_class_name('ytp-ad-button-text').text)
				print(wds.find_element_by_id('action-companion-click-target').find_element_by_id('header').text)
				print(wds.find_element_by_id('domain').text)
				print(wds.find_element_by_class_name('ytp-ad-player-overlay-instream-info').find_element_by_class_name('ytp-ad-button-text').text)
				time.sleep(2)
			except:
				ads[len(ads)-1].append("display ad")
				ads[len(ads)-1].append(wds.find_element_by_id('action-companion-click-target').find_element_by_id('header').text)
				ads[len(ads)-1].append(wds.find_element_by_id('domain').text)
				print(wds.find_element_by_id('action-companion-click-target').find_element_by_id('header').text)
				print(wds.find_element_by_id('domain').text)
	else:
		try:
			wds.find_element_by_id('domain').text
			ads.append([])
			ads[len(ads)-1].append("display ad")
			ads[len(ads)-1].append(wds.find_element_by_id('action-companion-click-target').find_element_by_id('header').text)
			ads[len(ads)-1].append(wds.find_element_by_id('domain').text)
			print(wds.find_element_by_id('action-companion-click-target').find_element_by_id('header').text)
			print(wds.find_element_by_id('domain').text)
		except:
			print(' ')
	

#skip sec
def skip_sec(wds):
	vlen = v_len(wds)
	sec = str(random.randint(round((0.3*vlen)), round(0.8*vlen)))
	wds.execute_script('document.getElementsByTagName("video")[0].currentTime +='+sec)

#randomly assign sleep time in [a,b] range
def time_sleep(a,b):
	time.sleep(random.randint(a,b))

def skip_ad(wds):
	wds.find_element_by_class_name("ytp-ad-skip-button-container").click()


#after a video is openned what does a human do?
def human(wds):
	skip_sec(wds)
	time_sleep(3,6)


#fns1 = [skip_sec, time_sleep]
def to_do_ad(wds):
	l=len(ads)
	try:
		detect_ad(wds)
	except:
		time_sleep(3,5)
		detect_ad(wds)
	print(l)
	print(len(ads))
	if(len(ads)>l):
		try:
			skip_ad(wds)
		except:
			pass
	else:
		human(wds)
		detect_ad(wds)
		try:
			skip_ad(wds)
		except:
			time_sleep(4,10)
	time_sleep(2,5)
	try:
		play_next(driver)
	except:
		wds.back()

#player-ads
#sign in using eid
def sign_in(wds,eid):
	time.sleep(3)
	wds.find_element_by_xpath('//div[2]/ytd-button-renderer/a').click()
	time.sleep(5)
	email = wds.find_element_by_css_selector('input[type=email]')
	time.sleep(5)
	#eid = "juicewrldmx"
	for character in eid:
		email.send_keys(character)
		time.sleep(0.2)
	time.sleep(6)
	wds.find_element_by_id("identifierNext").click()
	time.sleep(random.randint(6,8))
	password = wds.find_element_by_css_selector('input[type=password]')
	time.sleep(random.randint(5,8))
	passkey = "10p15vp0011"
	for character in passkey:
		password.send_keys(character)
		time.sleep(0.2)
	time.sleep(random.randint(6,8))
	wds.find_element_by_id("passwordNext").click()
	time.sleep(random.randint(5,8))

fns = [search_click, home_page_1st_reco]
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1920x1080")

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()

driver = webdriver.Chrome(ChromeDriverManager().install())

time.sleep(random.randint(3,5))

n=2

while(len(ads)<n):
	driver.get('http://www.youtube.com')
	try:
		driver.get('http://www.youtube.com')
		sign_in(driver,eid)
		print("you're signed in")
	except:
		pass
	#driver.get('http://www.youtube.com')
	time.sleep(4)
	try:
		choice(fns)(driver)
	except:
		choice(fns)(driver)
	time_sleep(1,4)
	#home_page_1st_reco(driver)
	to_do_ad(driver)
	r = random.randint(1,4)
	for i in range(r):
		to_do_ad(driver)


a=[]

for i in range(len(ads)):
	for j in range(len(ads[i])):
		if len(ads[i][0]) == 0:
			ads[i][0] = 'video ad'
		if len(ads[i][1]) == 0:
			try:
				ads[i][1] = ads[i][2]
			except: 
				pass
	try:
		a=ads[i][1]
	except:
		pass
	try:
		ads[i][1]=ads[i][2]
	except:
		pass
	try:
		ads[i][2]=a
	except:
		pass


from datetime import date

today = date.today()


data1 = pd.DataFrame(ads, columns=['ads type', 'advertiser','advertisement'])

addate = pd.DataFrame([today]*data1.shape[0],columns=['date'])

data2 = pd.concat([addate,data1], axis=1)

with open('ads.csv', 'a') as f:
    f.write('\n')    
    

data2.to_csv('ads.csv', index = False, header = False, mode='a')

#cleaning advertisers

#b=[]
#for i in range(25):
#	b.append(len(ads[i]))
#c=0
#for i in range(len(b)):
#	if b[i]!=3:
#		c=i



#del ads[c]
















