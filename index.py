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

# CONFIG ***********************************************************************
#*******************************************************************************

main_channel = 'https://twitch.tv/seaofthieves'
watch_time_minutes = 20

# SETUP ************************************************************************
#*******************************************************************************

# configure edge driver **********************************************
#*********************************************************************

print('')
edge_options = EdgeOptions()
edge_options.use_chromium = True

for root, dirs, files in os.walk("extensions"):
	for name in files:
		full_extension_path = os.path.join(root, name)
		print("Adding Extension: " + full_extension_path)
		edge_options.add_extension(full_extension_path)

edge_options.add_argument('log-level=3')
# edge_options.add_argument('headless')
# edge_options.add_argument('disable-gpu')
driver = Edge(executable_path='drivers\\msedgedriver.exe', options=edge_options)

# flags **************************************************************
#*********************************************************************
last_hosted_url = 'none'

# # LIB ************************************************************************
# #*****************************************************************************

def print_header():
	print('')
	print('********************************************************************************')
	print('*')
	print('* Hosted/Raided Stream Auto-Watcher & Reward Claimer')
	print('*')
	print('* Author: Frosthaven#9900 (Discord)')
	print('*')
	print('* End Process with CTRL+C in this window')
	print('*')
	print('********************************************************************************')
	print('')

def browser_login_twitch():
	print_header()
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
		WebDriverWait(driver,8).until(
			EC.visibility_of_element_located((By.XPATH, "//button[@data-a-target='player-overlay-mature-accept']"))
		)
		driver.find_element(By.XPATH, "//button[@data-a-target='player-overlay-mature-accept']").click()
		print('clicked to allow mature content')
		WebDriverWait(driver,8).until(
			EC.invisibility_of_element_located((By.XPATH, "//button[@data-a-target='player-overlay-mature-accept']"))
		)
	except:
		print('no maturity notices to dismiss')
		pass

def await_watch_time_done():
	global watch_time_minutes
	print('staying in this channel for ' + str(watch_time_minutes) + ' minute(s)')
	time.sleep(watch_time_minutes*60)
	print('watch time completed')

def visit_main_channel():
	global main_channel
	print('navigating to seaofthieves channel')
	driver.get(main_channel)

	accept_mature_warning()

	print('waiting for new stream host...')

def visit_hosted_stream():
	global last_hosted_url
	global watch_time_minutes
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

		accept_mature_warning()
		await_watch_time_done()

		visit_main_channel()
	elif (stream_url != last_hosted_url):
		print('navigating to hosted channel: ' + stream_url)
		# new hosted stream found
		# last_hosted_url = stream_url
		driver.get(stream_url)

		accept_mature_warning()
		await_watch_time_done()

		visit_main_channel()
	else:
		print('still waiting on new stream host...')
		# not a new hosted stream
		time.sleep(5)

# # INIT ***********************************************************************
# #*****************************************************************************

running = True
try:
	browser_login_twitch()
	visit_main_channel()
	while (running):
		visit_hosted_stream()
except KeyboardInterrupt:
	running = False
	print('')
	print('process ended.')
	print('YOU CAN NOW CLOSE THIS TERMINAL')
	driver.quit()
	os._exit(1)


