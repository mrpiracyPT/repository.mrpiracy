#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2015 xsteal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json, re, xbmc, xbmcgui, os, sys, pprint, base64, math, string, socket, time
from . import jsunpack
from . import controlo
from random import randint
try:
	import urllib2
	import urlparse
	import htmlentitydefs
	import urllib
except:
	import urllib.request as urllib2
	from urllib.parse import urljoin as urlparse
	import html.entities as htmlentitydefs
	import urllib.parse as urllib


#from external.pyopenssl import SSL, crypto

#post: controlo.abrir_url(self.API_SITE+'login.php', post=post, header=controlo.headers)
#get: controlo.abrir_url(self.API_SITE+'eventos', header=controlo.headers)

class MyStream():
	def __init__(self, url):
		self.url = url
		self.UA = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"
		self.headers = {"User-Agent": self.UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
		self.legenda = ''

	def getId(self, url):
		return urlparse.urlparse(url).path.split("/")[-1]

	def abrirMyStream(self):
		return controlo.abrir_url(self.url, header=self.headers)

	def getMediaUrl(self):
		
		conteudo = self.abrirMyStream()
		result = re.findall("([$]=.+?\(\)\)\(\);)", conteudo, re.DOTALL)
		videoUrl = False
		if result:
			for i in result:
				decoded = self.temp_decode(i)
				if decoded:
					r = re.search("setAttribute\(\'src\', *\'([^']+)\'\)", decoded, re.DOTALL)
					if r:
						videoUrl = r.group(1)
		if videoUrl:
			return videoUrl+'|User-Agent=' + self.UA + '&Referer=' + self.url + '&Origin=https://embed.mystream.to'

		return ''


	def temp_decode(self, data):
		startpos = data.find('"\\""+') + 5
		endpos = data.find('"\\"")())()')
		first_group = data[startpos:endpos]
		l = re.search("(\(!\[\]\+\"\"\)\[.+?\]\+)", first_group, re.DOTALL)
		if l:
			first_group = first_group.replace(l.group(1), 'l').replace('$.__+', 't').replace('$._+', 'u').replace('$._$+', 'o')
			tmplist = []
			js = re.search('(\$={.+?});', data, re.DOTALL)
			if js:
				js_group = js.group(1)[3:][:-1]
				second_group = js_group.split(',')
				i = -1
				for x in second_group:
					a, b = x.split(':')
					if b == '++$':
						i += 1
						tmplist.append(("{}{}{}".format('$.', a, '+'), i))
					elif b == '(![]+"")[$]':
						tmplist.append(("{}{}{}".format('$.', a, '+'), 'false'[i]))
					elif b == '({}+"")[$]':
						tmplist.append(("{}{}{}".format('$.', a, '+'), '[object Object]'[i]))
					elif b == '($[$]+"")[$]':
						tmplist.append(("{}{}{}".format('$.',a,'+'),'undefined'[i]))
					elif b == '(!""+"")[$]':
						tmplist.append(("{}{}{}".format('$.', a, '+'), 'true'[i]))

				tmplist = sorted(tmplist, key=lambda x: str(x[1]))
				for x in tmplist:
					first_group = first_group.replace(x[0], str(x[1]))

				first_group = first_group.replace(r'\\"' , '\\').replace("\"\\\\\\\\\"", "\\\\").replace('\\"', '\\').replace('"', '').replace("+", "")
		try:
			final_data = unicode(first_group, encoding = 'unicode-escape')
			return final_data
		except:
			return False

	def getLegenda(self):
		return self.legenda


class Fembed():
	def __init__(self, url):
		self.oldUrl = url
		self.id = self.getId(url)
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
		self.legenda = ''
		req = urllib2.Request(url, headers=self.headers)
		response = urllib2.urlopen(req)
		self.url = response.geturl()
		response.close()
		self.host = re.findall(r'(?://|\.)([^/]+)', self.url)[0]
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0", "Referer": self.get_url(self.host,self.id)}

	def get_url(self, host, media_id):
		return 'https://{host}/v/{media_id}'.format(host=host, media_id=media_id)

	def getId(self, url):
		return urlparse.urlparse(url).path.split("/")[-1]

	def abrirMixdrop(self, url):
		return controlo.abrir_url(url, header=self.headers)

	def getMediaUrl(self):
		videoUrl = ''
		api_url = 'https://{0}/api/source/{1}'.format(self.host, self.id)
		post = {'r': '', 'd': self.host}
		post = json.dumps(post)

		responseUrl = ''
		#controlo.abrir_url(self.API_SITE+'login.php', post=post, header=controlo.headers)

		content, responseUrl = controlo.abrir_url(api_url, post=post, header=self.headers, retrieveUrl=True)

		if responseUrl != api_url:
			api_url = 'https://www.{0}/api/source/{1}'.format(self.host, self.id)
			content = controlo.abrir_url(api_url, post=post, header=self.headers)
		if content:
			js_data = json.loads(content)
			if js_data.get('success'):
				sources = [(i.get('label'), i.get('file')) for i in js_data.get('data') if i.get('type') == 'mp4']

				if len(sources) == 1:
					videoUrl = sources[0][1]
				elif len(sources) > 1:
					qualidade = xbmcgui.Dialog().select('Escolha a qualidade', [str(source[0]) if source[0] else 'Unknown' for source in sources])
					if qualidade == -1:
						controlo.log("ERRO")
					videoUrl = sources[qualidade][1]


		request = urllib2.Request(videoUrl)
		request.get_method = lambda: 'HEAD'
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0')
		for key in self.headers:
			request.add_header(key, self.headers[key])
		response = urllib2.urlopen(request)

		return videoUrl+'|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(self.headers[key])) for key in self.headers])
		
	def getLegenda(self):
		return self.legenda

class Mixdrop():
	def __init__(self, url):
		self.url = url
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
		self.legenda = ''

	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-1]

	def abrirMixdrop(self):
		headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
					'Cookie' : 'hds2=1' }
		return controlo.abrir_url(self.url, header=self.headers)

	def getHost(self):
		#return urlparse(self.url).netloc
		return urlparse(self.url, '/')

	def getMediaUrl(self):
		videoUrl = ''
		content = self.abrirMixdrop() 
		pattern = '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
		result = self.parse(content,pattern)
		controlo.log(self.getHost())
		headers = {'Origin': 'https://{0}'.format(self.getHost()), 'Referer': 'https://{0}/'.format(self.getHost()), 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}

		if result[0] == True:

			r = re.search(r'location\s*=\s*"([^"]+)', content)
			if r:
				web_url = 'https://{0}{1}'.format(self.getHost(), r.group(1))
				content = controlo.abrir_url(web_url, header=headers)

			if '(p,a,c,k,e,d)' in content:
				content = self.get_packed_data(content)
				#content = cPacker().unpack(result[1][0])

			#pattern = 'vsrc\d+="([^"]+)"'
			pattern = '(?:vsr|wurl|surl)[^=]*=\s*"([^"]+)'
			result = self.parse(content, pattern)
			if result[0] == True:
				videoUrl = result[1][0]
			#else:
			#	pattern = 'furl="([^"]+)"'
			#	result = self.parse(content, pattern)
			#	if result[0] == True:
			#		videoUrl = result[1][0]

			if videoUrl.startswith('//'):
				videoUrl = 'https:'+videoUrl

		return videoUrl

	def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
		sHtmlContent = self.replaceSpecialCharacters(str(sHtmlContent))
		aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
		if (len(aMatches) >= iMinFoundValue):
			return True, aMatches
		return False, aMatches

	def replaceSpecialCharacters(self, sString):
		return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'")

	def getLegenda(self):
		return self.legenda

	def get_packed_data(self, html):
		packed_data = ''
		for match in re.finditer(r'(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
			try:
				js_data = jsunpack.unpack(match.group(1))
				js_data = js_data.replace('\\', '')
				packed_data += js_data
			except:
				pass
		return packed_data

class Vidoza():
	def __init__(self, url):
		self.url = url
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}
		self.legenda = ''

	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-1]
	def abrirVidoza(self, url):
		headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
		return controlo.abrir_url('https://ooops.rf.gd/url.php?url=' + url, header=headers)
	

	def getMediaUrl(self):
		
		sourceCode = controlo.abrir_url(self.url, header=self.headers)

		try:
			sourceCode = sourceCode.decode('unicode_escape')
		except:
			pass		
		
		videoUrl = ''

		sPattern =  'src: *"([^"]+)".+?label:"([^"]+)"'
		aResult = self.parse(sourceCode, sPattern)
		self.legenda = ''
		if aResult[0]:
			links = []
			qualidades = []
			for aEntry in aResult[1]:
				links.append(aEntry[0])
				if aEntry[1] == '2160':
					qualidades.append('4K')
				else:
					qualidades.append(aEntry[1]+'p')

			if len(links) == 1:
				videoUrl = links[0]
			elif len(links) > 1:
				qualidade = xbmcgui.Dialog().select('Escolha a qualidade', qualidades)
				videoUrl = links[qualidade]
		videoUrl = videoUrl#+'|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(self.headers[key])) for key in self.headers])
		return videoUrl
	def getLegenda(self):
		return self.legenda
	def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
		sHtmlContent = self.replaceSpecialCharacters(str(sHtmlContent))
		aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
		if (len(aMatches) >= iMinFoundValue):
			return True, aMatches
		return False, aMatches
	def replaceSpecialCharacters(self, sString):
		return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'")

class CloudMailRu():
	def __init__(self, url):
		self.url = url
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}

	def getId(self):
		return re.compile('(?:\/\/|\.)cloud\.mail\.ru\/public\/(.+)').findall(self.url)[0]
	def getMediaUrl(self):

		headers = { 'Host': 'cloud.mail.ru',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'DNT': '1',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7' }

		sourceCode = controlo.abrir_url(self.url, header=headers)

		randomNumber = randint(1, 5)
		ext = re.compile('<meta name=\"twitter:image\" content=\"(.+?)\"/>').findall(sourceCode)[0]
		streamAux = controlo.clean(ext.split('/')[-1])
		extensaoStream = controlo.clean(streamAux.split('.')[-1])

		#token = re.compile('"tokens"\s*:\s*{\s*"download"\s*:\s*"([^"]+)').findall(conteudo)[0]
		"""mediaLink = ''
		try:
			mediaLink = re.compile('(https\:\/\/[a-zA-Z0-9\-\.]+cloud.+\.[a-zA-Z]{2,3}\/\S*?\/G)"').findall(sourceCode)[0]
		except:
			mediaLink = re.compile('(https\:\/\/[a-zA-Z0-9\-\.]+cloud.+\.[a-zA-Z]{2,3}(\/\S*)?\/weblink\/view\/)"').findall(sourceCode)[0][0]"""
		mediaLink = 'https://cloclo%s.cloud.mail.ru/weblink/view/' % (randomNumber)

		#videoUrl = '%s/%s?key=%s' % (mediaLink, self.getId(), token)
		videoUrl = '%s/%s' % (mediaLink, self.getId())
		return videoUrl, 'mp4'

#tknorris code: https://github.com/tknorris/script.module.urlresolver/

class CountdownDialog(object):
    __INTERVALS = 5
    
    def __init__(self, heading, line1='', line2='', line3='', active=True, countdown=60, interval=5):
        self.heading = heading
        self.countdown = countdown
        self.interval = interval
        self.line3 = line3
        if active:
            #if xbmc.getCondVisibility('Window.IsVisible(progressdialog)'):
            #    pd = ProgressDialog()
            #else:
            pd = xbmcgui.DialogProgress()
            if not self.line3: line3 = 'Expires in: %s seconds' % (countdown)
            pd.create(self.heading, line1, line2, line3)
            pd.update(100)
            self.pd = pd
        else:
            self.pd = None

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd
    
    def start(self, func, args=None, kwargs=None):
        if args is None: args = []
        if kwargs is None: kwargs = {}
        result = func(*args, **kwargs)
        if result:
            return result
        
        if self.pd is not None:
            start = time.time()
            expires = time_left = self.countdown
            interval = self.interval
            while time_left > 0:
                for _ in range(CountdownDialog.__INTERVALS):
                    xbmc.sleep(interval * 1000 / CountdownDialog.__INTERVALS)
                    if self.is_canceled(): return
                    time_left = expires - int(time.time() - start)
                    if time_left < 0: time_left = 0
                    progress = time_left * 100 / expires
                    line3 = 'Expires in: %s seconds' % (time_left) if not self.line3 else ''
                    self.update(progress, line3=line3)
                    
                result = func(*args, **kwargs)
                if result:
                    return result
    
    def is_canceled(self):
        if self.pd is None:
            return False
        else:
            return self.pd.iscanceled()
        
    def update(self, percent, line1='', line2='', line3=''):
        if self.pd is not None:
            self.pd.update(percent, line1, line2, line3)
class ResolverError(Exception):
    pass
