import requests
import json
import time
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = 'https://amazon.com'
TS = int(time.time())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_category_data():
	# Getting amazon site with chrome via selenium web driver
	options = Options()
	options.headless = True
	options.add_argument('--incognito')
	#options.add_argument('--headless')
	driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')
	driver.get(URL)
	driver.find_element_by_id("nav-hamburger-menu").click()
	driver.page_source
	html_page=driver.page_source
	soup = BeautifulSoup(html_page)


	for link in soup.find_all("a",  href=True):
#		links.append(a['href'])
		if link.text:
			status_code = make_request(str(link))
			if status_code == 200 :
				links = []
				links.append(link.get('href'))
				links.append(link.get("title"))
				links.append("OK")
				file_save(links)
			else:
				links = []
				links.append(link.get('href'))
				links.append(link.get("title"))
				links.append("Dead link")
				file_save(links)



def make_request(link):
	try:
		s = requests.Session()
		resp = s.get((('%s%s')%(URL,link)), headers=HEADERS)
		return resp.status_code
	except requests.exceptions.InvalidURL:
		print('invalid url: '+ link)
	except requests.exceptions.RequestException:
		print('invalid url: '+ link)
	except UnicodeError:
		print('invalid url: '+ link)

def file_save(content):
    with open(TS, "a+") as results:
        writer = csv.writer(results, delimiter=",")
        writer.writerow(content)



if __name__ == "__main__":
	get_category_data()

