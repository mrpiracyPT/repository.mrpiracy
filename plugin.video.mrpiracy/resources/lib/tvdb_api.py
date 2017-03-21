import os
import xbmcgui
import xbmc
import time
import urllib

import json

from bs4 import BeautifulSoup


 
class TVDB:

	def __init__(self, api_key, lingua):
		self.api_key = api_key
		self.lingua = lingua

	def abrir_url(url,postData=False):
		if postData:
			data = urllib.urlencode({'procurar' : postData})
			req = urllib2.Request(url,data)
		else: req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

	def getCurrentServerTime(self):
		url = abrir_url('http://thetvdb.com/api/Updates.php?type=none')
		soup = BeautifulSoup(abrir_url, 'xml')
		self.previoustime = soup.time
		return self.previoustime

	def getSerieId(self, idIMDb):
		url = abrir_url('http://www.thetvdb.com//api/GetSeriesByRemoteID.php?imdbid='+idIMDb+'&language='+self.lingua)
		soup = BeautifulSoup(abrir_url, 'xml')
		self.serieId = soup.find('seriesid').string
		self.serieName = soup.find('SeriesName').string
		return self.serieId

	def getSeasonEpisode(self, serieId, season, episode):
		url = abrir_url('http://thetvdb.com/api/'+self.api_key+'/series/'+serieId+'/default/'+season+'/'+episode+'/'+self.lingua+'.xml')
		soup = BeautifulSoup(abrir_url, 'xml')

		data = {}
		data['name'] = soup.find('EpisodeName').string
		data['overview'] = soup.find('Overview').string
		data['actors'] = soup.find('GuestStars').string
		data['aired'] = soup.find('FirstAired').string
		data['director'] = soup.fin('Director').string
		data['writer'] = soup.find('Writer').string
		data['poster'] = 'http://thetvdb.com/banners/'+soup.find('filename').string
		json_data = json.dumps(data)

		return json_data




