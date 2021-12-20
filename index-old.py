# CREDITS *********************************************************************
# Author: Shane "Frosthaven" Stanley <shane.stanley1983@gmail.com>
#
# This script will automatically watch 20 minutes of each streamer
# that SeaOfThieves hosts to gain the reward drops
#******************************************************************************

import re
import os
import sys
import glob
import shutil
import time
import datetime
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# SETUP ***********************************************************************
#******************************************************************************

edge_options = EdgeOptions()
edge_options.add_argument('log-level=3')
edge_options.use_chromium = True
# edge_options.add_argument('headless')
# edge_options.add_argument('disable-gpu')
driver = Edge(executable_path='drivers\\msedgedriver.exe', options=edge_options)

last_hosted_url = 'none'

# # LIB *************************************************************************
# #******************************************************************************

def browser_login_twitch():
	print('')
	print('*********************************************')
	print('*')
	print('* Sea of Thieves: Festival of Giving')
	print('* Hosted Stream Auto-Watcher')
	print('*')
	print('* Author: Frosthaven#9900 (Discord)')
	print('*')
	print('*********************************************')
	print('')
	print('launching twitch.tv')
	driver.get("https://twitch.tv/")

	# login
	print('please log in via the Edge browser to continue')
	driver.find_element(By.XPATH, "//button[@data-a-target='login-button']").click()
	WebDriverWait(driver,360).until(
		EC.presence_of_element_located((By.CLASS_NAME, "onsite-notifications"))
	)
	dismiss_modal()

def dismiss_modal():
	# click x on any modal
	try:
		WebDriverWait(driver,5).until(
			EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Close modal']"))
		)
		driver.find_element(By.XPATH, "//button[@aria-label='Close modal']").click()
		print('dismissed a modal popup')
	except:
		pass


def accept_mature_warning():
	# accept mature audiences warning
	print('checking for maturity warnings')
	try:
		WebDriverWait(driver,5).until(
			EC.visibility_of_element_located((By.XPATH, "//button[@data-a-target='player-overlay-mature-accept']"))
		)
		driver.find_element(By.XPATH, "//button[@data-a-target='player-overlay-mature-accept']").click()
		print('clicked to allow mature content')
	except:
		print('no maturity notices to dismiss')
		pass

def visit_seaofthieves():
	print('navigating to seaofthieves channel')
	driver.get("https://twitch.tv/seaofthieves")
	time.sleep(3)
	accept_mature_warning()
	time.sleep(3)
	print('waiting for new stream host...')
	visit_hosted_stream()

def visit_hosted_stream():
	global last_hosted_url
	try:
		WebDriverWait(driver,5).until(
			EC.visibility_of_element_located((By.XPATH, "//a[@data-a-target='hosting-indicator']"))
		)
		stream_url = driver.find_element(By.XPATH, "//a[@data-a-target='hosting-indicator']").get_attribute('href')
	except:
		stream_url = last_hosted_url
		pass

	current_url = driver.current_url

	if ('referrer=raid' in current_url):
		# user was redirected to a raided stream
		print('raid auto-redirect detected')
		current_url = current_url.replace('?referrer=raid','')
		print('Raiding: ' + current_url)
		last_hosted_url = current_url

		time.sleep(3)
		accept_mature_warning()
		time.sleep(3)

		print('staying in this channel for 20 minutes')

		# watch this stream for 20 minutes
		time.sleep(1200)

		# return to sea of thieves page
		print('watch time completed')
		visit_seaofthieves()
	elif (stream_url != last_hosted_url):
		print('navigating to hosted channel: ' + stream_url)
		# new hosted stream found
		last_hosted_url = stream_url
		driver.get(stream_url)
	
		time.sleep(3)
		accept_mature_warning()
		time.sleep(3)
		print('staying in this channel for 20 minutes')

		# watch this stream for 20 minutes
		time.sleep(1200)

		# return to sea of thieves page
		print('watch time completed')
		visit_seaofthieves()
	else:
		# not a new hosted stream
		time.sleep(10)
		visit_hosted_stream()



# # INIT ************************************************************************
# #******************************************************************************

browser_login_twitch()
visit_seaofthieves()

driver.quit()