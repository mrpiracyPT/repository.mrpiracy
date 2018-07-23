import os
import xbmcgui
import xbmc
import time
import urllib
import urllib2
import re

import json

from bs4 import BeautifulSoup


 
class TVDB:

	def __init__(self, api_key, lingua):
		self.api_key = api_key
		self.lingua = lingua

	def abrir_url(self, url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

	def getCurrentServerTime(self):
		url = self.abrir_url('http://thetvdb.com/api/Updates.php?type=none')
		soup = BeautifulSoup(url)
		self.previoustime = soup.time
		return self.previoustime

	def getSerieInfo(self, idIMDb):

		url = self.abrir_url('http://www.thetvdb.com/api/GetSeriesByRemoteID.php?imdbid='+idIMDb+'&language='+self.lingua)
		soup = BeautifulSoup(url)

		data = {}
		data["serieId"] = soup.seriesid.text
		data["poster"] = 'http://thetvdb.com/banners/'+soup.banner.text
		data["aired"] = soup.firstaired.text
		data["plot"] = soup.overview.text
		return json.dumps(data)

	def getSerieId(self, idIMDb):
		url = self.abrir_url('http://www.thetvdb.com/api/GetSeriesByRemoteID.php?imdbid='+idIMDb+'&language='+self.lingua)
		soup = BeautifulSoup(url)
		return soup.seriesid.text


	def getSeasonEpisodio(self, idIMDb, season, episodio):
		serieId = self.getSerieId(idIMDb)
		url = self.abrir_url('http://thetvdb.com/api/'+self.api_key+'/series/'+str(serieId)+'/default/'+str(season)+'/'+str(episodio)+'/'+self.lingua+'.xml')
		soup = BeautifulSoup(url)

		data = {}
		data['name'] = soup.episodename.text
		data['plot'] = soup.overview.text
		data['actors'] = soup.gueststars.text
		data['aired'] = soup.firstaired.text
		data['director'] = soup.director.text
		data['writer'] = soup.writer.text
		data['poster'] = 'http://thetvdb.com/banners/'+soup.filename.text
		data['season'] = season
		data['episode'] = episodio
		json_data = json.dumps(data)

		return json_data




