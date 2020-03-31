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

import json, re, xbmc, urllib, xbmcgui, os, sys, pprint, urlparse, urllib2, base64, math, string, socket
import htmlentitydefs
from cPacker import cPacker
from t0mm0.common.net import Net
import jsunpacker
from AADecoder import AADecoder
from JsParser import JsParser
from JJDecoder import JJDecoder
from cPacker import cPacker
from png import Reader as PNGReader
from HTMLParser import HTMLParser
import controlo
import time

import HTMLParser

#from external.pyopenssl import SSL, crypto

def clean(text):
    command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def log(msg, level=xbmc.LOGNOTICE):
	level = xbmc.LOGNOTICE
	print('[MRPIRACY]: %s' % (msg))

	try:
		if isinstance(msg, unicode):
			msg = msg.encode('utf-8')
		xbmc.log('[MRPIRACY]: %s' % (msg), level)
	except Exception as e:
		try:
			a=1
		except: pass  

class Mixdrop():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
		self.legenda = ''

	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-1]

	def abrirMixdrop(self):
		headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
					'Cookie' : 'hds2=1' }
		req = urllib2.Request(self.url, headers=self.headers)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

	def getMediaUrl(self):
		videoUrl = ''
		content = self.abrirMixdrop() 
		pattern = '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
		result = self.parse(content,pattern)

		if result[0] == True:
			content = cPacker().unpack(result[1][0])

			#pattern = 'vsrc\d+="([^"]+)"'
			pattern = 'wurl="([^"]+)"'
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



class Streamango():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
		self.legenda = ''

	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-2]
	def abrirStreamango(self, url):
		headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
		req = urllib2.Request('https://ooops.rf.gd/url.php?url=' + url, headers=headers)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	def decode(self, encoded, code):
		#from https://github.com/jsergio123/script.module.urlresolver - kodi vstream
		_0x59b81a = ""
		k = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
		k = k[::-1]

		count = 0

		for index in range(0, len(encoded) - 1):
			while count <= len(encoded) - 1:
				_0x4a2f3a = k.index(encoded[count])
				count += 1
				_0x29d5bf = k.index(encoded[count])
				count += 1
				_0x3b6833 = k.index(encoded[count])
				count += 1
				_0x426d70 = k.index(encoded[count])
				count += 1

				_0x2e4782 = ((_0x4a2f3a << 2) | (_0x29d5bf >> 4))
				_0x2c0540 = (((_0x29d5bf & 15) << 4) | (_0x3b6833 >> 2))
				_0x5a46ef = ((_0x3b6833 & 3) << 6) | _0x426d70
				_0x2e4782 = _0x2e4782 ^ code

				_0x59b81a = str(_0x59b81a) + chr(_0x2e4782)

				if _0x3b6833 != 64:
					_0x59b81a = str(_0x59b81a) + chr(_0x2c0540)
				if _0x3b6833 != 64:
					_0x59b81a = str(_0x59b81a) + chr(_0x5a46ef)

		return _0x59b81a

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.url, headers=self.headers).content.decode('unicode_escape')
		
		videoUrl = ''
		resultado = re.search("{type:\"video/mp4\",src:\w+\('([^']+)',(\d+)", sourceCode)

		if resultado:
			source = self.decode(resultado.group(1), int(resultado.group(2)))
			
			if source.endswith('@'):
				source = source[:-1]
			source = "http:%s" % source # if source.startswith("//") else source
			#source = source.split("/")
			"""if not source[-1].isdigit():
				source[-1] = re.sub('[^\d]', '', source[-1])
			videoUrl = "/".join(source)"""

		return source

		
	def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
		sHtmlContent = self.replaceSpecialCharacters(str(sHtmlContent))
		aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
		if (len(aMatches) >= iMinFoundValue):
			return True, aMatches
		return False, aMatches
	def getLegenda(self):
		return self.legenda
	def replaceSpecialCharacters(self, sString):
		return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'")


class Vidoza():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}
		self.legenda = ''

	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-1]
	def abrirVidoza(self, url):
		headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
		req = urllib2.Request('https://ooops.rf.gd/url.php?url=' + url, headers=headers)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.url, headers=self.headers).content.decode('unicode_escape')
		
		
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


class RapidVideo():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}
		self.legenda = ''

	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-1]
	def abrirRapidVideo(self, url):
		headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
		req = urllib2.Request('https://ooops.rf.gd/url.php?url=' + url, headers=headers)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	

	def getMediaUrl(self):
		try:
			#sourceCode = self.abrirRapidVideo(self.url).decode('unicode_escape')
			sourceCode = self.net.http_GET(self.url, headers=self.headers).content.decode('unicode_escape')
			
		except:
			#sourceCode = self.abrirRapidVideo(self.url)
			headers = { 'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
			sourceCode = controlo.abrir_url('https://ooops.rf.gd/url.php?url=' + self.url, header=headers)
			html_parser = HTMLParser.HTMLParser()
			sourceCode = html_parser.unescape(sourceCode)
			
			#sourceCode = self.net.http_GET(self.url, headers=self.headers).content
	
		
		videoUrl = ''
		sPattern = '<input type="hidden" value="(\d+)" name="block">'
		aResult1 = self.parse(sourceCode,sPattern)
		if (aResult1[0] == True):
			sourceCode = self.net.http_POST(self.url, 'confirm.x=74&confirm.y=35&block=1', headeres=self.headers)

		sPattern =  '"file":"([^"]+)","label":"([0-9]+)p.+?'
		aResult = self.parse(sourceCode, sPattern)
		try:
			self.legenda = "https://www.raptu.com%s"%re.compile('"file":"([^"]+)","label":".+?","kind":"captions"').findall(sourceCode)[0]
			#log(self.legenda)
		except:
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
				links.reverse()
				qualidades.reverse()

				qualidade = xbmcgui.Dialog().select('Escolha a qualidade', qualidades)
				videoUrl = links[qualidade]
		
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
		self.net = Net()
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}

	def getId(self):
		return re.compile('(?:\/\/|\.)cloud\.mail\.ru\/public\/(.+)').findall(self.url)[0]
	def getMediaUrl(self):

		headers = { 'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		  'Host': ' cloud.mail.ru',
		  'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' }
		   
		req = urllib2.Request(self.url, headers=headers)
		response = urllib2.urlopen(req)  
		sourceCode = response.read()
		response.close()

		ext = re.compile('<meta name=\"twitter:image\" content=\"(.+?)\"/>').findall(sourceCode)[0]
		streamAux = clean(ext.split('/')[-1])
		extensaoStream = clean(streamAux.split('.')[-1])
		#token = re.compile('"tokens"\s*:\s*{\s*"download"\s*:\s*"([^"]+)').findall(conteudo)[0]
		mediaLink = re.compile('(https\:\/\/[a-zA-Z0-9\-\.]+cldmail+\.[a-zA-Z]{2,3}\/\S*)"').findall(sourceCode)[0]
		#videoUrl = '%s/%s?key=%s' % (mediaLink, self.getId(), token)
		videoUrl = '%s/%s' % (mediaLink, self.getId())
		return videoUrl, extensaoStream

class GoogleVideo():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}
		self.UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-2]

	def getMediaUrl(self):
		req = urllib2.Request(self.url)
		response = urllib2.urlopen(req)  
		sourceCode = response.read()
		Headers = response.headers
		response.close()
		try:
			sourceCode = sourceCode.decode('unicode_escape')
		except:
			pass
		c = Headers['Set-Cookie']
		c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',c)
		if c2:
			cookies = ''
			for cook in c2:
				cookies = cookies + cook[0] + '=' + cook[1]+ ';'

		formatos = {
		'5': {'ext': 'flv'},
		'6': {'ext': 'flv'},
		'13': {'ext': '3gp'},
		'17': {'ext': '3gp'},
		'18': {'ext': 'mp4'},
		'22': {'ext': 'mp4'},
		'34': {'ext': 'flv'},
		'35': {'ext': 'flv'},
		'36': {'ext': '3gp'},
		'37': {'ext': 'mp4'},
		'38': {'ext': 'mp4'},
		'43': {'ext': 'webm'},
		'44': {'ext': 'webm'},
		'45': {'ext': 'webm'},
		'46': {'ext': 'webm'},
		'59': {'ext': 'mp4'}
		}
		formatosLista = re.search(r'"fmt_list"\s*,\s*"([^"]+)', sourceCode).group(1)
		formatosLista = formatosLista.split(',')
		streamsLista = re.search(r'"fmt_stream_map"\s*,\s*"([^"]+)', sourceCode).group(1)
		streamsLista = streamsLista.split(',')

		videos = []
		qualidades = []
		i = 0
		for stream in streamsLista:
			formatoId, streamUrl = stream.split('|')
			form = formatos.get(formatoId)
			extensao = form['ext']
			resolucao = formatosLista[i].split('/')[1]
			largura, altura = resolucao.split('x')
			if 'mp' in extensao or 'flv' in extensao:
				qualidades.append(altura+'p '+extensao)
				videos.append(streamUrl)
				i+=1
		qualidade = xbmcgui.Dialog().select('Escolha a qualidade', qualidades)
		return videos[qualidade]+'|User-Agent=' + self.UA + '&Cookie=' + cookies, qualidades[qualidade].split('p ')[-1]


class UpToStream():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}

	def getId(self):
		if 'iframe' in self.url:
			return re.compile('http\:\/\/uptostream\.com\/iframe\/(.+)').findall(self.url)[0]
		else:
			return re.compile('http\:\/\/uptostream\.com\/(.+)').findall(self.url)[0]

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.url, headers=self.headers).content

		links = re.compile('source\s+src=[\'\"]([^\'\"]+)[\'\"].+?data-res=[\'\"]([^\"\']+)[\'\"]').findall(sourceCode)
		videos = []
		qualidades = []
		for link, qualidade in links:
			if link.startswith('//'):
				link = "http:"+link
			videos.append(link)
			qualidades.append(qualidade)
		videos.reverse()
		qualidades.reverse()
		qualidade = xbmcgui.Dialog().select('Escolha a qualidade', qualidades)
		return videos[qualidade]

class OpenLoad():

	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.id = str(self.getId())
		self.messageOk = xbmcgui.Dialog().ok
		self.site = 'https://openload.co'
		#self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Referer': url}

	#Código atualizado a partir de: https://github.com/Kodi-vStream/venom-xbmc-addons/ 
	def ASCIIDecode(self, string):
    
		i = 0
		l = len(string)
		ret = ''
		while i < l:
			c =string[i]
			if string[i:(i+2)] == '\\x':
				c = chr(int(string[(i+2):(i+4)],16))
				i+=3
			if string[i:(i+2)] == '\\u':
				cc = int(string[(i+2):(i+6)],16)
				if cc > 256:
					#ok c'est de l'unicode, pas du ascii
					return ''
				c = chr(cc)
				i+=5     
			ret = ret + c
			i = i + 1

		return ret

	def __getHost(self):
		parts = self.url.split('//', 1)
		host = parts[0]+'//'+parts[1].split('/', 1)[0]
		return host
	def SubHexa(self, g):
		return g.group(1) + self.Hexa(g.group(2))
    
	def Hexa(self, string):
		return str(int(string, 0))

	def parseInt(self, sin):
		return int(''.join([c for c in re.split(r'[,.]',str(sin))[0] if c.isdigit()])) if re.match(r'\d+', str(sin), re.M) and not callable(sin) else None

	def CheckCpacker(self, str):

		sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
		aResult = re.findall(sPattern,str)
		if (aResult):
			str2 = aResult[0]
			if not str2.endswith(';'):
				str2 = str2 + ';'
			try:
				str = cPacker().unpack(str2)
				print('Cpacker encryption')
			except:
				pass

		return str
	    
	def CheckJJDecoder(self, str):

		sPattern = '([a-z]=.+?\(\)\)\(\);)'
		aResult = re.findall(sPattern,str)
		if (aResult):
			print('JJ encryption')
			return JJDecoder(aResult[0]).decode()

		return str
    
	def CheckAADecoder(self, str):
		aResult = re.search('([>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)', str,re.DOTALL | re.UNICODE)
		if (aResult):
			print('AA encryption')
			tmp = aResult.group(1) + AADecoder(aResult.group(2)).decode()
			return str[:aResult.start()] + tmp + str[aResult.end():]

		return str
    
	def CleanCode(self, code,Coded_url):
		#extract complete code
		r = re.search(r'type="text\/javascript">(.+?)<\/script>', code,re.DOTALL)
		if r:
			code = r.group(1)

		#1 er decodage
		code = self.ASCIIDecode(code)

		#fh = open('c:\\html2.txt', "w")
		#fh.write(code)
		#fh.close()

		#extract first part
		P3 = "^(.+?)}\);\s*\$\(\"#videooverlay"
		r = re.search(P3, code,re.DOTALL)
		if r:
			code = r.group(1)
		else:
			log('er1')
			return False
		    
		#hack a virer dans le futur
		code = code.replace('!![]','true')
		P8 = '\$\(document\).+?\(function\(\){'
		code= re.sub(P8,'\n',code)
		P4 = 'if\(!_[0-9a-z_\[\(\'\)\]]+,document[^;]+\)\){'
		code = re.sub(P4,'if (false) {',code)
		P4 = 'if\(+\'toString\'[^;]+document[^;]+\){'
		code = re.sub(P4,'if (false) {',code)

		#hexa convertion
		code = re.sub('([^_])(0x[0-9a-f]+)',self.SubHexa,code)
		 
		#Saut de ligne
		#code = code.replace(';',';\n')
		code = code.replace('case','\ncase')
		code = code.replace('}','\n}\n')
		code = code.replace('{','{\n')

		#tab
		code = code.replace('\t','')

		#hack
		code = code.replace('!![]','true')

		return code
	def __replaceSpecialCharacters(self, sString):
		return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'")

	def parserOPENLOADIO(self, urlF):
		try:
			req = urllib2.Request(urlF, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0'})
			response = urllib2.urlopen(req)
			html = response.read()
			response.close()
			try: html = html.encode('utf-8')
			except: pass

			TabUrl = []
			sPattern = '<p id="([^"]+)" *style=\"\">([^<]+)<\/p>'
			aResult = self.parse(html, sPattern)
			if not aResult[0]:
				sPattern = '<p style="" *id="([^"]+)" *>([^<]+)<\/p>'
				aResult = self.parse(html, sPattern)
			if (aResult[0]):
				TabUrl = aResult[1]
			else:
				#log("No Encoded Section Found. Deleted?")
				raise ResolverError('No Encoded Section Found. Deleted?')
			sPattern = '<script src="\/assets\/js\/video-js\/video\.js.+?.js"(.+)*'
			aResult = self.parse(html, sPattern)
			if (aResult[0]):
				sHtmlContent2 = aResult[1][0]
			code = ''
			maxboucle = 4
			sHtmlContent3 = sHtmlContent2
			while (maxboucle > 0):
				sHtmlContent3 = self.CheckCpacker(sHtmlContent3)
				sHtmlContent3 = self.CheckJJDecoder(sHtmlContent3)
				sHtmlContent3 = self.CheckAADecoder(sHtmlContent3)
				maxboucle = maxboucle - 1
			code = sHtmlContent3
			
			id_final = ""
			sPattern = 'var srclink.*?\/stream\/.*?(#[^\'"]+).*?mime=true'
			aResult = re.findall(sPattern, code)

			if (aResult):
				id_final = aResult[0]
			else:
				raise ResolverError('No Encoded Section Found. Deleted?')

			if not (code):
				#log("No Encoded Section Found. Deleted?")
				raise ResolverError('No Encoded Section Found. Deleted?')
			
			Coded_url = ''
			for i in TabUrl:
				if len(i[1]) > 30:
					Coded_url = i[1]
					Item_url = '#'+ i[0]
			if not(Coded_url):
				raise ResolverError('No Encoded Section Found. Deleted?')

			code = self.CleanCode(code, Coded_url)

			xbmc.executebuiltin("Notification(%s,%s,%s)" % ("MrPiracy", "A Descomprimir Openload, aguarde!", 15000))
			JP = JsParser()
			Liste_var = []
			JP.AddHackVar(Item_url, Coded_url)
			JP.ProcessJS(code,Liste_var)
			url = None
			try:
				url = JP.GetVarHack(id_final)
			except:
				raise ResolverError('No Encoded Section Found. Deleted?')
			

			if not(url):
				raise ResolverError('No Encoded Section Found. Deleted?')
			api_call =  self.__getHost()+"/stream/" + url + "?mime=true" 
			

			if 'KDA_8nZ2av4/x.mp4' in api_call:
				#log('Openload.co resolve failed')
				raise ResolverError('Openload.co resolve failed')
			if url == api_call:
				#log('pigeon url : ' + api_call)
				api_call = ''
				raise ResolverError('pigeon url : ' + api_call)
			
			return api_call
		#ResolverError, 
		except (Exception, ResolverError):
			try:
				media_id = self.getId()
				log("API OPENLOAD")
				video_url = self.__check_auth(media_id)
				if not video_url:
					video_url = self.__auth_ip(media_id)
				
				if video_url:
					return video_url
				else:
					raise ResolverError("Sem autorização do Openload")
			except ResolverError:
				self.messageOk('MrPiracy', 'Ocorreu um erro a obter o link. Escolha outro servidor.')
		
	def _api_get_url(self, url):
		
		result = self.net.http_GET(url).content
		
		js_result = json.loads(result)
		if js_result['status'] != 200:
			raise ResolverError(js_result['status'], js_result['msg'])
		return js_result
	def __auth_ip(self, media_id):
		js_data = self._api_get_url('https://api.openload.co/1/streaming/info')
		pair_url = js_data.get('result', {}).get('auth_url', '')
		if pair_url:
			pair_url = pair_url.replace('\/', '/')
			header = "Autorização do Openload"
			line1 = "Para visualizar este video, é necessaria autorização"
			line2 = "Acede ao link em baixo para permitires acesso ao video:"
			line3 = "[B][COLOR blue]%s[/COLOR][/B] e clica em 'Pair'" % (pair_url)
			with CountdownDialog(header, line1, line2, line3) as cd:
				return cd.start(self.__check_auth, [media_id])
	
	def __check_auth(self, media_id):
		try:
			js_data = self._api_get_url('https://api.openload.co/1/streaming/get?file=%s' % media_id)
		except ResolverError as e:
			status, msg = e
			if status == 403:
				return
			else:
				raise ResolverError(msg)	


		return js_data.get('result', {}).get('url')
	def getId(self):
		#return self.url.split('/')[-1]
		try:
			try:
				return re.compile('https\:\/\/openload\.co\/embed\/(.+)\/').findall(self.url)[0]
			except:
				return re.compile('https\:\/\/openload\.co\/embed\/(.+)').findall(self.url)[0]
		except:
			return re.compile('https\:\/\/openload.co\/f\/(.+?)\/').findall(self.url)[0]


	def unescape(self, text):
		def fixup(m):
			text = m.group(0)
			if text[:2] == "&#":
				try:
					if text[:3] == "&#x":
						return unichr(int(text[3:-1], 16))
					else:
						return unichr(int(text[2:-1]))
				except ValueError:
					pass
			else:
				try:
					text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
				except KeyError:
					pass
				return text # leave as is
		return re.sub("&#?\w+;", fixup, text)

	def getMediaUrl(self):

		videoUrl = self.parserOPENLOADIO(self.url)

		return videoUrl

	def getDownloadUrl(self):
		content = self.net.http_GET(self.url, headers=self.headers).content

		url = self.decodeOpenLoad(str(content.encode('utf-8')))

		return url

	def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
		sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
		aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
		if (len(aMatches) >= iMinFoundValue):
			return True, aMatches
		return False, aMatches
	
	def parseInt(self, sin):
		return int(''.join([c for c in re.split(r'[,.]',str(sin))[0] if c.isdigit()])) if re.match(r'\d+', str(sin), re.M) and not callable(sin) else None

	def getSubtitle(self):
		pageOpenLoad = self.net.http_GET(self.url, headers=self.headers).content

		try:
			subtitle = re.compile('<track\s+kind="captions"\s+src="(.+?)"').findall(pageOpenLoad)[0]
		except:
			subtitle = ''
		#return self.site + subtitle
		return subtitle


class VideoMega():

	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.id = str(self.getId())
		self.messageOk = xbmcgui.Dialog().ok
		self.site = 'https://videomega.tv'
		self.headers = 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
		self.headersComplete = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25', 'Referer': self.getNewHost()}

	def getId(self):
		return re.compile('http\:\/\/videomega\.tv\/view\.php\?ref=(.+?)&width=700&height=430').findall(self.url)[0]

	def getNewHost(self):
		return 'http://videomega.tv/cdn.php?ref=%s' % (self.id)

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.getNewHost(), headers=self.headersComplete).content
		match = re.search('<source\s+src="([^"]+)"', sourceCode)

		if match:
			return match.group(1) + '|User-Agent=%s' % (self.headers)
		else:
			self.messageOk('MrPiracy.xyz', 'Video nao encontrado.')

class Vidzi():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.id = str(self.getId())
		self.messageOk = xbmcgui.Dialog().ok
		self.site = 'https://videomega.tv'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
		self.subtitle = ''

	def getId(self):
		return re.compile('http\:\/\/vidzi.tv\/embed-(.+?)-').findall(self.url)[0]

	def getNewHost(self):
		return 'http://vidzi.tv/embed-%s.html' % (self.id)

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.getNewHost(), headers=self.headers).content

		if '404 Not Found' in sourceCode:
			self.messageOk('MrPiracy.win', 'Ficheiro nao encontrado ou removido. Escolha outro servidor.')

		match = re.search('file\s*:\s*"([^"]+)', sourceCode)
		if match:
			return match.group(1) + '|Referer=http://vidzi.tv/nplayer/jwpayer.flash.swf'
		else:
			for pack in re.finditer('(eval\(function.*?)</script>', sourceCode, re.DOTALL):
				dataJs = jsunpacker.unpack(pack.group(1)) # Unpacker for Dean Edward's p.a.c.k.e.r | THKS

				#print dataJs
				#pprint.pprint(dataJs)

				stream = re.search('file\s*:\s*"([^"]+)', dataJs)
				try:
					subtitle = re.compile('tracks:\[\{file:"(.+?)\.srt"').findall(dataJs)[0]
					subtitle += ".srt"
				except:
					try:
						subtitle = re.compile('tracks:\[\{file:"(.+?)\.vtt"').findall(dataJs)[0]
						subtitle += ".vtt"
					except:
						subtitle = ''
				self.subtitle = subtitle

				if stream:
					return stream.group(1)

		self.messageOk('MrPiracy.win', 'Video nao encontrado. Escolha outro servidor')


	def getSubtitle(self):
		return self.subtitle

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
