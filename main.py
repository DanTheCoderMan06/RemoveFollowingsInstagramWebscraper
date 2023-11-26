import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
from dotenv import load_dotenv,dotenv_values
import requests
from pathlib import Path
#imports
load_dotenv(dotenv_path=Path('config.env'))
with open('config.env') as fp:
	print(fp.read())
opt = Options()
amountofpeopleunfollowed = 1
LONG_TIMEOUT = 30
opt.detach = False
driver = webdriver.Firefox(options=opt)
driver.get("http://www.instagram.com")
dontunfollow=json.loads(os.getenv('DONT_UNFOLLOW'))
#System Variables
print('Log in !')
time.sleep(int(os.getenv('WAIT_UNTIL_LOGGED_IN')))
unfollowapp = driver.find_element(By.XPATH, f"//div[@class='_aano']").find_elements(By.TAG_NAME,"div")[0]
while True:
	scrollingframe=unfollowapp.find_element(By.XPATH, ".//div[@style='display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;']")
	allrequests = driver.find_elements(By.XPATH,'.//div[@class="x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3"]')
	print(len(allrequests))
	for frame in allrequests:
		try:
			button = frame.find_element(By.XPATH,'.//button[@class=" _acan _acap _acat _aj1- _ap30"]')
			text = button.find_element(By.XPATH,'.//div[@class="_ap3a _aaco _aacw _aad6 _aade"]').get_attribute("innerHTML").strip()
			username = frame.find_element(By.XPATH,'.//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade"]').get_attribute("innerHTML").strip().lower()
			if text == 'Following' and username not in dontunfollow:
				button.click()
				unfollowbutton = WebDriverWait(driver, LONG_TIMEOUT).until(
					EC.presence_of_element_located((By.XPATH, './/button[@class="_a9-- _ap36 _a9-_"]'))
				)
				unfollowbutton.click()
				print(f'UNFOLLOWED{username} COUNT SINCE START:{amountofpeopleunfollowed}')
				if os.getenv('ENABLE_DISCORD') == 'True':
					requests.post(os.getenv('DISCORD_WEBHOOK'),json={'content' : f'UNFOLLOWED{username} COUNT SINCE START:{amountofpeopleunfollowed}'})
				WebDriverWait(driver, LONG_TIMEOUT
					).until_not(EC.presence_of_element_located((By.XPATH, './/button[@class="_a9-- _ap36 _a9-_"]')))
				time.sleep(int(os.getenv('UNFOLLOW_WAIT')))
				amountofpeopleunfollowed += 1 
		except:
			pass
	driver.execute_script("arguments[0].scrollIntoView({block: 'end', behavior: 'smooth'});", unfollowapp) #Refresh
	time.sleep(int(os.getenv('REFRESH_UNFOLLOW_LIST')))