import os
import re
import pysubs2
import requests
import pysrt
from bs4 import BeautifulSoup

def resync(name, second=15, encoding='utf-8'):
	if name.split('.')[-1] == 'srt': 
		sub = pysrt.open(name, encoding=encoding)
		sub.shift(seconds=second)
		sub.save()
	if name.split('.')[-1] == 'ass':
		sub = pysubs2.load(name, encoding=encoding)
		sub.shift(s=second)
		sub.save(name)

def rename(vid, sub):
	if len(vid) != len(sub):
		print("Error file length!")
		return False
	for i in range(len(sub)):
		os.renames(sub[i], vid[i][:-3] + sub[i][-3:])

def series(vid, name, start, season):
	title = name.title()
	post = vid[0].split('.')[-1]
	for count, file in enumerate(vid):
		os.renames(file, "%s S%.2d E%.2d.%s" % (title, season, count+start, post))
def add_name(vid, sub):
	for counter, file in enumerate(vid):
		name = '.'.join(file.split('.')[:-1])
		os.renames(file, "%s - %s.mkv" % (name, sub[counter]))
def getvid():
	vid = sorted_alphanumeric([file for file in os.listdir() if 'mkv' in file])
	return vid
def getsub():
	sub = sorted_alphanumeric([file for file in os.listdir() if 'srt' in file])
	return sub
def sorted_alphanumeric(data):
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(data, key=alphanum_key)
def imdb_get(url):
	proxies = {
	    'http': 'socks5://127.0.0.1:9050',
	    'https': 'socks5://127.0.0.1:9050'
	}
	result = requests.get(url)
	soup = BeautifulSoup(result.content, features='html5lib')
	sub = [title['title'] for title in soup.find_all('a', attrs={'itemprop' :"name"})]
	return sub

def auto_name(vid, name, start, season, url):
	series(vid, name, start, season)
	vid = getvid()
	sub = imdb_get(url)
	add_name(vid, sub)
