def resync(name, encoding=''):
	if name.split('.')[-1] == 'srt': 
		import pysrt
		encoding = 'windows-1256' if encoding is '' else encoding
		sub = pysrt.open(name, encoding=encoding)
		sub.shift(seconds=15.5)
		sub.save()
	if name.split('.')[-1] == 'ass':
		import pysubs2
		encoding = "utf-8" if encoding == '' else encoding
		sub = pysubs2.load(name, encoding=encoding)
		sub.shift(s=15.5)
		sub.save(name)

def rename(vid, sub):
	import os
	for i in range(len(sub)):
		os.renames(sub[i], vid[i][:-3] + sub[i][-3:])

def series(vid, name, start, season):
	import os
	title = name.title()
	post = vid[0].split('.')[-1]
	for count, file in enumerate(vid):
		os.renames(file, "%s S%.2d E%.2d.%s" % (title, season, count+start, post))
def add_name(vid, sub):
	import os
	for counter, file in enumerate(vid):
		name = '.'.join(file.split('.')[:-1])
		os.renames(file, "%s - %s.mkv" % (name, sub[counter]))
def getvid():
	import os
	vid = sorted_alphanumeric([file for file in os.listdir() if 'mkv' in file])
	return vid
def getsub():
	import os
	sub = sorted_alphanumeric([file for file in os.listdir() if 'srt' in file])
	return sub
def sorted_alphanumeric(data):
	import re
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(data, key=alphanum_key)
def imdb_get(url):
	import requests
	from bs4 import BeautifulSoup
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
