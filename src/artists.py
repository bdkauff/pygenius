# -*- coding: utf-8 -*-

import sys
import re
import pageopen

def albumList(query, arg='titles'):
#returns a list of album titles or links to the album on rapgenius.

	albums = []
	links = []

	query = '-'.join(query.split())
	url = "http://rapgenius.com/artists/%s" % query
	soup = pageopen.openPage(url)
	text = soup.find_all(class_="album_link")

	l = len(text)

	for i in range(0, l):
		raw = str(text[i])
		raw = raw.replace('<a class="album_link" href="', '')
		raw = raw.replace('">', ',')
		raw = raw.replace('</a>', '')
		new = raw.split(',')

		album = new[1]
		albums.append(album)
		
		link = 'http://rapgenius.com%s' % new[0]
		links.append(link)

	if (arg == 'links'):
		return links
	else:
		return albums

def returnDates(query):
	#returning album names and dates they were released.
	titles = albumList(query, 'titles')
	links = albumList(query, 'links')

	l = len(links)

	dates = []
	info = []

	for i in range(0, l):

		url = links[i]
		soup = pageopen.openPage(url)
		names = soup.find_all('h1', class_="name")

		k = len(names)

		for j in range(0, k):
			date = str(names[j])
			date = ' '.join(date.split())
			search1 = date.find('(1')
			search2 = date.find('(2')
			if search1 != -1:
				date = '1'+ date.split('(1')[1] #strip everything before the date
				date = date.split(')')[0] #stripping everything after the date
				dates.append(date)
			elif search2 != -1:
				date = '2'+ date.split('(2')[1] #strip everything before the date
				date = date.split(')')[0] #stripping everything after the date
				dates.append(date)
			else:
				dates.append('None')

		info.append([titles[i], dates[i]])

	return info

#returns metadata about an album: description, track number, and track name
def getAlbumData(artist, query):

	tracks = []

	artistlink = '-'.join(artist.split())
	query = '-'.join(query.split())
	url = "http://rapgenius.com/albums/%s/%s" % (artistlink, query)

	soup = pageopen.openPage(url)
	meta = soup.find_all(property="og:description")
	text = soup.find_all(class_="song_name")

	meta = str(meta)
	meta = re.sub(r'\<.*?\"', '', meta)
	meta = re.sub(r'\" .*?\>', '', meta)
	tracks.append(meta)

	l = len(text)

	for i in range(0, l):
		trackNo = i+1
		track = str(text[i])
		track = re.sub(r'\<.*?\>', '', track)
		track = ' '.join(track.split())
		track = track.split('– ')[1]
		track = track.split(' Lyrics')[0]
		tracks.append([trackNo, track])
	
	return tracks
	

#returns an artist's bio
def getArtistBio(artist):
	print "Working on it!"

