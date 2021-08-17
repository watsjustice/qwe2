import json
import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from fake_useragent import UserAgent
import re

def get_html(url):

	try:
		driver = webdriver.Chrome(
			executable_path = 'C:/Users/Денис/Desktop/Web/parser1/chromedriver.exe'
		)

		driver.get(url)
		sleep(3)

		with open('html_selenium.html', "w", encoding="utf-8") as f:
			f.write(driver.page_source)

	except Exception as ex:
		print(ex)

	finally:
		driver.close()
		driver.quit()

	with open('html_selenium.html') as f:
		r = f.read()
	return r
	
def get_data_basic_stat():
	data_titles = [

		'Elapsed' , 'Half time' , 'Full time',
		'Kick off' , ' Date'	
	]

	k = 1

	headers = {}
	r = get_html('https://1xbet.whoscored.com/Matches/1549539/Live/England-Premier-League-2021-2022-Brentford-Arsenal')
	soup = BeautifulSoup(r, 'lxml').find_all(class_ = 'info-block cleared')

	flag = True
	k , q = len(soup) , 1

	for item , object in zip(soup , range(k) ):
 

		if flag:
			headers[str(item.find('dt').text)[:-1]] = str(item.find('dd').text)

		else:
			headers[str(item.find('dt').text)[:-1]] =  str(item.find('dd').text)
			flag = True


		if len(item.find_all('dt')) == 2:
			if len(item.find_all('dd')) == 2:

				headers[''.join(re.split('<dt>|</dt>', str(item.find('dt').find_next_sibling('dt'))))] = ''.join(re.split('<dd>|</dd>', str(item.find('dd').find_next_sibling('dd'))))

				flag = False
				q += 1

	with open ('match-static.json' , 'w') as f:
		json.dump(headers , f , indent = 4 , ensure_ascii = False)

def get_data_add_stat():

	r = get_html('https://1xbet.whoscored.com/Matches/1549539/Live/England-Premier-League-2021-2022-Brentford-Arsenal')

	soup = BeautifulSoup(r , 'lxml').find(class_ = 'grid').find_all('tr')
	data = {}

	home_ancidents , away_ancidents = [] , []

	for home in soup:
		
		if home.find(class_ = 'key-incident home-incident'):
			home = home.find(class_ = 'key-incident home-incident')
			home_ancidents += [home]

	for away in soup:

		if away.find(class_ = 'key-incident away-incident'):
			away = away.find(class_ = 'key-incident away-incident')
			away_ancidents += [away]

	data_item = {}		
	q_time = ''
	object_add = ''
	object = ''

	# скретчинг колонки -- HOME
	for item_home in home_ancidents:
	
		try:
			if item_home.find(class_ = 'match-centre-header-team-key-incident has-related-event').get('title'):
				object = str(item_home.find(class_ = 'match-centre-header-team-key-incident has-related-event').get('title'))
				name = item_home.find(class_ = 'player-name').text

				try:
					object_add_name = item_home.find(class_= 'match-centre-header-team-key-incident has-related-event').find(class_ = 'player-name').text
				except:
					pass

				#остальные колонки с 2+ событиями
				if len(item_home.find_all(class_ = 'match-centre-header-team-key-incident has-related-event')) > 1:
					object_add_name = item_home.find(class_ = 'match-centre-header-team-key-incident has-related-event').find_next_sibling('div').find(class_ = 'player-name').text
					object_add = item_home.find(class_ = 'match-centre-header-team-key-incident has-related-event').find_next_sibling('div').get('title')

				if 'GOAL!' in object and 'Assisted' in object:
					object = f'GOAL by {object_add_name} assisted by {name}'
				
				if 'GOAL!' in object and 'Assisted' not in object:
					object = f'GOAL by {name}'



				q_time = int(item_home.find(class_ = 'incident-icon').get('data-minute'))+1
				data_item[object , object_add] = q_time


		except:
			object = ''
			q_time = ''
			object_add_name = ''
			object_add = ''
			try:
				theonlyone = item_home.find(class_='match-centre-header-team-key-incident').get('title')
				theonlyone_name = item_home.find(class_='match-centre-header-team-key-incident').find(class_ = 'player-name').text

				if 'GOAL!' in theonlyone and 'Assisted' not in theonlyone:
					object = f'GOAL by {theonlyone_name}'

				q_time = int(item_home.find(class_ = 'incident-icon').get('data-minute'))+1
				data_item[object , object_add] = q_time

			except:
				pass

	data_item_1 = {}		
	q_time = ''
	object_add = ''
	object = ''

	# скретчинг колонки -- AWAY
	for item_away in away_ancidents:
		try:
			if item_away.find(class_ = 'match-centre-header-team-key-incident has-related-event').get('title'):
				object = str(item_away.find(class_ = 'match-centre-header-team-key-incident has-related-event').get('title'))
				name = item_away.find(class_ = 'player-name').text



				try:
					object_add_name = item_away.find(class_= 'match-centre-header-team-key-incident has-related-event').find(class_ = 'player-name').text
				except:
					pass

				#остальные колонки с 2+ событиями
				if len(item_away.find_all(class_ = 'match-centre-header-team-key-incident has-related-event')) > 1:
					object_add_name = item_away.find(class_ = 'match-centre-header-team-key-incident has-related-event').find_next_sibling('div').find(class_ = 'player-name').text
					object_add = item_away.find(class_ = 'match-centre-header-team-key-incident has-related-event').find_next_sibling('div').get('title')


				if 'GOAL!' in object and 'Assisted' in object:
					object = f'GOAL by {object_add_name} assisted by {name}'
				
				if 'GOAL!' in object and 'Assisted' not in object:
					object = f'GOAL by {name}'



				q_time = int(item_away.find(class_ = 'incident-icon').get('data-minute'))+1
				data_item_1[object , object_add] = q_time


		except:
			object = ''
			q_time = ''
			object_add_name = ''
			object_add = ''
			try:
				theonlyone = item_away.find(class_='match-centre-header-team-key-incident').get('title')
				theonlyone_name = item_away.find(class_='match-centre-header-team-key-incident').find(class_ = 'player-name').text

				if 'GOAL!' in theonlyone and 'Assisted' not in theonlyone:
					object = f'GOAL by {theonlyone_name}'

				q_time = int(item_away.find(class_ = 'incident-icon').get('data-minute'))+1
				data_item_1[object , object_add] = q_time

			except:
				pass		
	data = {}
	datacheck = []
	datacheck1 = set()


	for i in data_item.values():
		for o in data_item_1.values():
			datacheck1.add(i)
			datacheck1.add(o)

	datacheck1 = sorted(datacheck1)


	for x in range(len(data_item.keys())+2):
		try:
			data[datacheck1[x]] = str(list(data_item.keys())[list(data_item.values()).index(datacheck1[x])])
		except:
			pass

	for x in range(len(data_item_1.keys())+2):
		try:
			data[datacheck1[x]] += ' : '
			data[datacheck1[x]] += str(list(data_item_1.keys())[list(data_item_1.values()).index(datacheck1[x])])
		except:
			pass


	with open('f_ancidents.json', 'w') as f:
		json.dump(data , f  , indent = 4 , ensure_ascii = False)

get_data_add_stat()
get_data_basic_stat()

