#!/usr/bin/python
# -*- coding: utf-8 -*-


import urlparse,json,zlib,hashlib,time,re,os,sys,xbmc,xbmcgui,xbmcplugin,xbmcvfs,pprint, base64,urllib
import unicodedata
import controlo
import Player
import URLResolverMedia
import Downloader
import Database
import Trakt
import definicoes
import ast
reload(sys)  
sys.setdefaultencoding('utf8')
class mrpiracy:

	def __init__(self):
		self.API = base64.urlsafe_b64decode('aHR0cDovL21yYXBpLnh5ei8=')
		self.API_SITE = base64.urlsafe_b64decode('aHR0cDovL21yYXBpLnh5ei9hcGluZXcv')#aHR0cDovL21wYXBpLm1sL2FwaS8=
		self.SITE = base64.urlsafe_b64decode('aHR0cDovL21ycGlyYWN5LmdxLw==')
	def definicoes(self):
		controlo.addon.openSettings()
		controlo.addDir('Entrar novamente','url', 'inicio', os.path.join(controlo.artFolder, controlo.skin, 'retroceder.png'))
		#vista_menu()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
	def menu(self):
		login = self.login()
		database = Database.criarFicheiros()

		if login:
			#evento = self.getEventos()
			#if evento:
				#controlo.addDir('[B]'+evento+'[/B]', self.API_SITE+'evento/1', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
				#controlo.addDir('', '', '', os.path.join(controlo.artFolder, controlo.skin, 'nada.png'))
			controlo.addDir('Filmes', self.API_SITE+'filmes', 'menuFilmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
			controlo.addDir('Séries', self.API_SITE+'series', 'menuSeries', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
			controlo.addDir('Animes', self.API_SITE+'animes', 'menuAnimes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
			controlo.addDir('Pesquisa', self.API_SITE+'pesquisa.php', 'pesquisa', os.path.join(controlo.artFolder, controlo.skin, 'procurar.png'))
			controlo.addDir('', '', '', os.path.join(controlo.artFolder, controlo.skin, 'nada.png'))
			if Trakt.loggedIn():
				self.getTrakt()
				#+ self.getNumNotificacoes()   ---- controlo.addDir('Trakt', self.API_SITE+'me', 'menuTrakt', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
			controlo.addDir('A Minha Conta ', self.API_SITE+'me', 'conta', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			controlo.addDir('Definições', self.API_SITE, 'definicoes', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			
			
		else:
			controlo.addDir('Alterar Definições', 'url', 'definicoes', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			controlo.addDir('Entrar novamente', 'url', 'inicio', os.path.join(controlo.artFolder, controlo.skin, 'retroceder.png'))
		definicoes.vista_menu()
	def loginTrakt(self):
		Trakt.traktAuth()
	def getTrakt(self):
		url = 'https://api-v2launch.trakt.tv/users/%s/watched/movies' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		filmes = Trakt.getTrakt(url, login=False)
		url = 'https://api-v2launch.trakt.tv/users/%s/watched/shows' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		series = Trakt.getTrakt(url, login=False)
		#insertTraktDB(filmes, series, data)
		url = 'https://api-v2launch.trakt.tv/sync/watchlist/movies'
		watchlistFilmes = Trakt.getTrakt(url)
		url = 'https://api-v2launch.trakt.tv/sync/watchlist/shows'
		watchlistSeries = Trakt.getTrakt(url)
		url = 'https://api-v2launch.trakt.tv/users/%s/watched/shows' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		progresso = Trakt.getTrakt(url, login=False)
		Database.insertTraktDB(filmes, series, watchlistFilmes, watchlistSeries, progresso, controlo.dataHoras)
	def menuFilmes(self):
		controlo.addDir('Todos os Filmes', self.API_SITE+'filmes.php?qualidade='+definicoes.getQualidade(), 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		#controlo.addDir('Filmes em Destaque', self.API_SITE+'filmes/destaque', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		controlo.addDir('Filmes por Ano', self.API_SITE+'filmes.php?action=ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Filmes por Genero', self.API_SITE+'filmes.php?action=categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		#controlo.addDir('Filmes por Ranking IMDB', self.API_SITE+'filmes/imdbRank/qualidade/'+definicoes.getQualidade(), 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		#controlo.addDir('Filmes para Crianças', self.API_SITE+'filmes/pt/qualidade/'+definicoes.getQualidade(), 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		definicoes.vista_menu()
	def menuTrakt(self):
		controlo.addDir('Progresso', self.API_SITE+'filmes', 'progressoTrakt', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Watchlist Filmes', self.API_SITE+'filmes/destaque', 'traktWatchlistFilmes', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Watchlist Series', self.API_SITE+'filmes/ano', 'traktWatchlistSeries', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Listas Pessoais', self.API_SITE+'filmes/ano', 'traktListas', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		definicoes.vista_menu()
	def menuSeries(self):
		controlo.addDir('Todas as Séries', self.API_SITE+'series.php', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		#controlo.addDir('Séries em Destaque', self.API_SITE+'series/destaque', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		controlo.addDir('Séries por Ano', self.API_SITE+'series.php?action=ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Séries por Genero', self.API_SITE+'series.php?action=categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		#controlo.addDir('Séries por Ranking IMDB', self.API_SITE+'series/imdbRank', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		definicoes.vista_menu()
	def menuAnimes(self):
		controlo.addDir('Todos os Animes', self.API_SITE+'animes.php', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
		#controlo.addDir('Animes em Destaque', self.API_SITE+'animes/destaque', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
		controlo.addDir('Animes por Ano', self.API_SITE+'animes.php?action=ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Animes por Genero', self.API_SITE+'animes.php?action=categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		#controlo.addDir('Animes por Ranking IMDB', self.API_SITE+'animes/imdbRank', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		definicoes.vista_menu()
	def conta(self):
		controlo.addDir('Favoritos', self.API_SITE+'favoritos.php', 'favoritosMenu', os.path.join(controlo.artFolder, controlo.skin, 'favoritos.png'))
		controlo.addDir('Agendados', self.API_SITE+'verdepois.php', 'verdepoisMenu', os.path.join(controlo.artFolder, controlo.skin, 'agendados.png'))
		#controlo.addDir('Notificações', self.API_SITE+'index.php?action=notificacoes', 'notificacoes', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))
		#controlo.addDir('Mensagens', self.API_SITE+'index.php?action=mensagens', 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))
		definicoes.vista_menu()
	def favoritosMenu(self):
		controlo.addDir('Filmes Favoritos', self.API_SITE+'favoritos.php?action=filmes&qualidade='+definicoes.getQualidade(), 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'fifav.png'))
		controlo.addDir('Séries Favoritas', self.API_SITE+'favoritos.php?action=series', 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'sefav.png'))
		controlo.addDir('Animes Favoritos', self.API_SITE+'favoritos.php?action=animes', 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'anfav.png'))
		definicoes.vista_menu()
	def verdepoisMenu(self):
		controlo.addDir('Filmes Agendados', self.API_SITE+'verdepois.php?action=filmes&qualidade='+definicoes.getQualidade(), 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'fiagend.png'))
		controlo.addDir('Séries Agendadas', self.API_SITE+'verdepois.php?action=series', 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'seagend.png'))
		controlo.addDir('Animes Agendados', self.API_SITE+'verdepois.php?action=animes', 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'anagend.png'))
		definicoes.vista_menu()

	def login(self):
		
		if controlo.addon.getSetting('email') == '' or controlo.addon.getSetting('password') == '':
			controlo.alerta('MrPiracy', 'Precisa de definir o seu email e password')
			return False
		else:
			try:
				post = urllib.urlencode({'username': controlo.addon.getSetting('email'), 'password': controlo.addon.getSetting('password') })

				resultado = controlo.abrir_url(self.API_SITE+'login.php', post=post, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False

				try:
					resultado = resultado.decode('utf-8')
				except:
					resultado = resultado.encode('utf-8')
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'definicoes.mrpiracy'), resultado)
				resultado = json.loads(resultado)

				
				try:
					if resultado['codigo'] == 204:
						controlo.alerta('MrPiracy', resultado['mensagem'])
						return False
				except:
					pass
				token = resultado['cookie']
				refresh = resultado['expira']

				if resultado['vistos_filmes'] != "" or resultado['vistos_filmes'] != []:
					try:
						vistos_filmes = ','.join(ast.literal_eval(resultado['vistos_filmes'].replace('"', "'")).values())
					except:
						vistos_filmes = str(0)
				else:
					vistos_filmes = str(0)
				
				if resultado['vistos_series'] != "" or resultado['vistos_series'] != []:
					try:
						vistos_series = ','.join(ast.literal_eval(resultado['vistos_series']).values())
					except:
						vistos_series= str(0)
				else:
					vistos_series=str(0)
				if resultado['ver_depois'] != "" or resultado['ver_depois'] != []:
					try:
						#ver_depois = ','.join(ast.literal_eval(json.dumps(resultado['ver_depois'])).values())
						ver_depois = ','.join(map(str, resultado['ver_depois']))

					except:
						ver_depois = str(0)
				else:
					ver_depois = str(0)
				if resultado['favoritos'] != "" or resultado['favoritos'] != []:
					try:
						#favoritos = ','.join(ast.literal_eval(json.dumps(resultado['favoritos'])).values())
						favoritos = ','.join(map(str, resultado['favoritos']))
					except:
						favoritos = str(0)
				else:
					favoritos = str(0)
				categorias = resultado['categorias']
				try:
					username = resultado['username'].decode('utf-8')
				except:
					username = resultado['username'].encode('utf-8')
				
				
				
				xbmc.executebuiltin("XBMC.Notification(MrPiracy, Sessão iniciada: "+username+", '10000', "+controlo.addonFolder+"/icon.png)")
				controlo.addon.setSetting('tokenMrpiracy', token)
				controlo.addon.setSetting('refreshMrpiracy', refresh)
				controlo.addon.setSetting('loggedin', username)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'vistos_filmes.mrpiracy'), vistos_filmes)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'vistos_series.mrpiracy'), vistos_series)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.mrpiracy'), ver_depois)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'favoritos.mrpiracy'), favoritos)

				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'categorias.mrpiracy'), str(categorias))
				
				return True
			except:
				controlo.alerta('MrPiracy', 'Não foi possível abrir a página. Por favor tente novamente')
				return False
		"""else:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy, Sessão iniciada: "+username+", '10000', "+controlo.addonFolder+"/icon.png)")
			return True"""
	def getEventos(self):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(self.API_SITE+'eventos', header=controlo.headers)
		resultado = json.loads(resultado)
		try:
			if resultado['codigo'] == 204:
				return False
		except:
			pass
		return resultado['data']['nome']
	def getNumNotificacoes(self):
		"""controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultado = controlo.abrir_url(self.API_SITE+'me', header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)"""
		devolve = '[B][COLOR red]'
		devolve += str(controlo.addon.getSetting('notificacoes'))+' notificacoes e '+str(controlo.addon.getSetting('mensagens'))+' mensagens'
		devolve += '[/COLOR][/B]'
		return devolve
	
	def getFavoritos(self,id):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'favoritos.mrpiracy')).split(",")
		devolve = False
		if lista == "" or lista == [] or lista == '[]':
			return devolve
		for x in lista:
			if id==x:
				devolve = True
		return devolve
	
	def getVerDepois(self,id):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.mrpiracy')).split(",")
		devolve = False

		if lista == "" or lista == [] or lista == '[]':
			return devolve
		for x in lista:
			if id==x:
				devolve = True
		return devolve
	
	def getVistoEpisodio(self,id):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'vistos_series.mrpiracy')).split(",")
		devolve = False
		if lista == "" or lista == [] or lista == '[]':
			return devolve
		for x in lista:
			if id==x:
				devolve = True
		return devolve
	
	def getVistoFilme(self,id):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'vistos_filmes.mrpiracy')).split(",")
		devolve = False
		if lista == "" or lista == [] or lista == '[]':
			return devolve
		
		for x in lista:
			if id==x:
				devolve = True
		return devolve

	def favoritos(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		#controlo.log(url)
		if 'filmes' in url:
			tipo = 'filmes'
		elif 'series' in url:
			tipo = 'series'
		elif 'animes' in url:
			tipo = 'animes'
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if tipo == 'filmes':
			for i in resultado['data']:
				self.setFilme(i, vistos, opcao)
		elif tipo == 'series' or tipo == 'animes':
			for i in resultado['data']:
				self.setSeries(i, vistos, opcao, tipo)
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total):
			controlo.addDir('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
		definicoes.vista_filmesSeries()
	def verdepois(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if 'filmes' in url:
			tipo = 'filmes'
		elif 'series' in url:
			tipo = 'series'
		elif 'animes' in url:
			tipo = 'animes'
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if tipo == 'filmes':
			for i in resultado['data']:
				self.setFilme(i, vistos, opcao)
				
		elif tipo == 'series' or tipo == 'animes':
			for i in resultado['data']:
				self.setSeries(i, vistos, opcao, tipo)
		
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total):
			controlo.addDir('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
		definicoes.vista_filmesSeries()
	def notificacoes(self, url):
		resultadoa = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		#controlo.log(resultadoa)
		resultadoa = json.loads(resultadoa)
		vistosF = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		for i in resultadoa["data"]:
			if i['tipoVideo'] == 'filme':
				resultado = controlo.abrir_url(self.API_SITE+'filme/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				self.setFilme(i, vistos, opcao)
			elif i['tipoVideo'] == ('serie' or 'anime'):
				resultado = controlo.abrir_url(self.API_SITE+i['tipoVideo']+'/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				tipo = tipo+'s'
				self.setSeries(i, vistos, opcao, tipo)

		"""current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'notificacoes', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))"""
		definicoes.vista_menu()

	def mensagens(self, url):
		resultadoa = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		#controlo.log(resultadoa)
		resultadoa = json.loads(resultadoa)
		for i in resultadoa["data"]:
			controlo.addDir(i['mensagem'], url, 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))

		"""current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))"""
		definicoes.vista_menu()
	def filmes(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		for i in resultado['data']:
			self.setFilme(i, vistos, opcao)			
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total):
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
		definicoes.vista_filmesSeries()
	def series(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		for i in resultado['data']:
			self.setSeries(i, vistos, opcao, tipo)
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total):
			controlo.addDir('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 'series', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
		definicoes.vista_filmesSeries()
	def temporadas(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)['data'][0]
		id = url.split('=')[-1]
		
		if 'serie' in url:
			url = self.API_SITE+'series.php?action=temporada&idSerie='+id+'&n=%s'
		elif 'anime' in url:
			url = self.API_SITE+'animes.php?action=temporada&idSerie='+id+'&n=%s'
		try:
			resultado['temporadas'] = resultado['temporadas'].replace('especial', '999')
		except:
			pass
		if resultado['temporadas'] == "":
			return False
		for c, i in sorted(json.loads(resultado['temporadas']).iteritems(), key=lambda i: int(i[0])):
			if c != '999':
				controlo.addDir("[B]Temporada[/B] "+str(c), (url % str(c)), 'episodios', os.path.join(controlo.artFolder, controlo.skin,'temporadas', 'temporada'+str(c)+'.png'),poster=self.API+resultado['background'])
			else:
				controlo.addDir("[B]Temporada Especial[/B]", (url % '999'), 'episodios', os.path.join(controlo.artFolder, controlo.skin,'temporadas', 'temporadaEspecial.png'),poster=self.API+resultado['background'])

		definicoes.vista_temporadas()
	def episodios(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		
		"""controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		resultadoS = controlo.abrir_url(self.API_SITE+tipo+'/'+url.split('/')[5], header=controlo.headers)
		resultadoS = json.loads(resultadoS)"""
		vistos = Database.selectSeries()
		opcao = controlo.addon.getSetting('marcarVisto')
		naoVisto = False
		numeroParaVer = 0
		temporadaParaVer = 0
		serieParaVer = 0
		episodioParaVer = 0
		contagem = 0
		for i in resultado['data']:
		
			pt = ''
			infoLabels = {'Title': i['nome_episodio'], 'Code': i['IMBD'], 'Episode': i['episodio'], 'Season': i['temporada'] }
			try:
				nome = i['nome_episodio'].decode('utf-8')
			except:
				nome = i['nome_episodio'].encode('utf-8')
			br = ''
			final = ''
			semLegenda = ''
			if i['fimtemporada'] == "1":
				final = '[B]Final da Temporada [/B]'
			if i['semlegenda'] == "1":
				semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
			if 'PT' in i['IMBD']:
				i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			imdbSerie = i['fotoSerie'].split('/')[-1].split('.')[0]
			vistoe = False
			cor = 'white'
			visto = False
			vistoa = False
			if opcao == '1' or opcao == '2':
				if self.getVistoEpisodio(i['id_episodio']) == 1:
					vistoa = True
			elif opcao == '0' or opcao == '2':
				vistoa = self.verificarVistoLocal(i['id_serie'], temporada=i['temporada'], episodio=i['episodio'])
			
			if Trakt.loggedIn():			
				ep = i['episodio']
				if '/' in i['episodio']:
					ep = i['episodio'].split('/')[0]
				if 'e' in i['episodio']:
					ep = i['episodio'].split('e')[0]
				for v in json.loads(vistos):
					if v["show"]["ids"]["imdb"] is None:
						visto = False
						continue
					if v["show"]["ids"]["imdb"] != imdbSerie:
						visto = False
						continue
					else:
						for s in v["seasons"]:
							if int(s['number']) == int(i['temporada']):
								for e in s['episodes']:
									if int(e["number"]) == int(ep):
										vistoe = True
										break
									else:
										vistoe = False
			
			if vistoa:
				visto = True
			else:
				visto = False
						
			if vistoe:
				visto = True
				cor = 'blue'
			if visto == False and vistoe == False:
				if naoVisto == False:
					numeroParaVer = i['episodio']
					temporadaParaVer = i['temporada']
					serieParaVer = i['id_serie']
					episodioParaVer = i['id_episodio']
					serieAVer = i['id_serie']
					naoVisto = True
			else:
				contagem = contagem + 1

			imagem = ''
			if i['imagem'] == "1":
				imagem = self.API+'images/series/'+i['IMBD']+'.jpg'
			elif i['imagem'] == "0":
				imagem = self.API+'images/capas/'+imdbSerie+'.jpg'
			
			controlo.addVideo(pt+br+final+semLegenda+'[COLOR '+cor+'][B]Episodio '+str(i['episodio'])+'[/B][/COLOR] '+nome, self.API_SITE+tipo+'.php?action=episodio&idSerie='+str(i['id_serie'])+'&idEpisodio='+str(i['id_episodio']), 'player', imagem, visto, 'episodio', i['temporada'], i['episodio'], infoLabels, self.API+i['background'])
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total):
			controlo.addDir('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 'episodios', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
		definicoes.vista_episodios()
		if naoVisto == True:
			if controlo.addon.getSetting('nao-visto-episodios') == 'true':
				if contagem > 0:
					pergunta = controlo.simNao('MrPiracy', 'Carregar o Episódio #'+str(numeroParaVer)+' da temporada #'+str(temporadaParaVer)+'?')
					if pergunta:
						self.player(self.API_SITE+tipo+'.php?action=episodio&idSerie='+str(serieAVer)+'&idEpisodio='+str(episodioParaVer))
		
	def listagemAnos(self, url):
		anos = [
			'2020',
			'2019',
			'2018',
			'2017',
			'2016',
			'2015',
			'2014',
			'2013',
			'2012',
			'2011',
			'2010',
			'2009',
			'2008',
			'2007',
			'2006',
			'2000-2005',
			'1990-1999',
			'1980-1989',
			'1970-1979',
			'1960-1969',
			'1950-1959',
			'1900-1949'
		]
		if 'filmes' in url:
			tipo = 0
			qualidade = '&qualidade='+definicoes.getQualidade()
		elif 'series' in url:
			tipo = 1
			qualidade = ''
		elif 'animes' in url:
			tipo = 2
			qualidade = ''
		for i in anos:
			controlo.addDir(i, url+'&ano='+i+qualidade, 'anos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		definicoes.vista_menu()
	def listagemGeneros(self, url):
		lista = definicoes.getListCategoria()
		if 'filmes' in url:
			tipo = 0
			qualidade = '&qualidade='+definicoes.getQualidade()
		elif 'series' in url:
			tipo = 1
			qualidade = ''
		elif 'animes' in url:
			tipo = 2
			qualidade = ''
		
		for c in ast.literal_eval(lista):
			if c['id_categoria'] == "0":
				continue
			try:
				cat = c['categorias'].decode('utf-8')
			except:
				cat = c['categorias'].encode('utf-8')
			controlo.addDir(cat, url+'&categoria='+str(c['id_categoria'])+qualidade, 'categorias', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		definicoes.vista_menu()
	def anos(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultadoa = json.loads(resultado)
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		for i in resultadoa["data"]:
			if 'filme' in url:
				self.setFilme(i, vistos, opcao)
			elif 'serie' in url or 'anime' in url:
				self.setSeries(i, vistos, opcao, tipo)
		current = resultadoa['meta']['current']
		total = resultadoa['meta']['total']
		try: proximo = resultadoa['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total):
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'anos', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
		definicoes.vista_filmesSeries()
		
	def categorias(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultadoa = json.loads(resultado)
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		for i in resultadoa["data"]:
			if 'filme' in url:
				self.setFilme(i, vistos, opcao)
			elif 'serie' in url or 'anime' in url:
				self.setSeries(i, vistos, opcao, tipo)
		current = resultadoa['meta']['current']
		total = resultadoa['meta']['total']
		try: proximo = resultadoa['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total):
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'categorias', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))

		definicoes.vista_filmesSeries()
	def player(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)[0]
		infolabels = dict()
		
		if 'filme' in url:
			tipo = 'filme'
			infolabels['Code'] = resultado['IMBD']
			infolabels['Year'] = resultado['ano']
			idVideo = resultado['id_video']
			nome = resultado['nome_ingles']
			temporada = 0
			episodio = 0
			coiso = 'filme'
			_imdb = resultado['IMBD']
		else:
			if 'serie' in url:
				tipo = 'serie'
			else:
				tipo = 'anime'
			idVideo = resultado['id_episodio']
			nome = resultado['nome_episodio']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			_imdb = resultado['fotoSerie'].split('/')[-1].split('.')[0]
			coiso = 'outro'
			

		controlo.mensagemprogresso.create('MrPiracy', u'Abrir emissão','Por favor aguarde...')
		controlo.mensagemprogresso.update(25, "", u'Obter video e legenda', "")
		stream, legenda, ext_g = self.getStreamLegenda(idVideo, tipo, coiso=coiso)
		if stream == False and legenda == 204:
			controlo.mensagemprogresso.close()
			controlo.alerta('MrPiracy', 'Tem de esperar 8 horas até conseguir visualizar algum video.')
			return False
		controlo.mensagemprogresso.update(50, "", u'Prepara-te, vai começar!', "")
		playlist = xbmc.PlayList(1)
		playlist.clear()
		iconimage = ''

		listitem = xbmcgui.ListItem(nome, iconImage="DefaultVideo.png", thumbnailImage=iconimage)

		#liz.setInfo( type="Video", infoLabels=infolabels )
		listitem.setInfo(type="Video", infoLabels=infolabels)
		#listitem.setInfo("Video", {"title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		listitem.setPath(path=stream)
		playlist.add(stream, listitem)

		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

		controlo.mensagemprogresso.update(75, "", u'Boa Sessão!!!', "")

		if stream == False:
			controlo.mensagemprogresso.close()
			controlo.alerta('MrPiracy', 'O servidor escolhido não disponível, escolha outro ou tente novamente mais tarde.')
		else:

			player_mr = Player.Player(url=url, idFilme=idVideo, pastaData=controlo.pastaDados, temporada=temporada, episodio=episodio, nome=nome, logo=os.path.join(controlo.addonFolder,'icon.png'), imdb=_imdb)

			controlo.mensagemprogresso.close()
			player_mr.play(playlist)
			player_mr.setSubtitles(legenda)

			while player_mr.playing:
				xbmc.sleep(5000)
				player_mr.trackerTempo()

	def getStreamLegenda(self, id, tipo, coiso=None):

		if tipo == 'filme':
			url = self.API_SITE+tipo+'s.php?action=links&idFilme='+id
		if tipo == 'serie':
			url = self.API_SITE+tipo+'s.php?action=links&idEpisodio='+id
		if tipo == 'anime':
			url = self.API_SITE+tipo+'s.php?action=links&idEpisodio='+id

		#controlo.log(url)
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		try:
			if resultado['codigo'] == 204:
				return False, 204, 204
		except: 
			resultado = resultado[0]

		i = 0
		servidores = []
		titulos = []
		nome = ''
		if resultado['URL'] != '':
			i+=1
			if 'openload' in resultado['URL'].lower():
				nome = "OpenLoad"
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidzi' in resultado['URL'].lower():
				nome = 'Vidzi'
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'google' in resultado['URL'].lower() or 'cloud.mail.ru' in resultado['URL'].lower():
				nome = 'MrPiracy'
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'uptostream.com' in resultado['URL'].lower():
				nome = 'UpToStream'
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'rapidvideo.com' in resultado['URL'].lower() or 'raptu' in resultado['URL'].lower():
				nome = 'Raptu'
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidoza.net' in resultado['URL'].lower():
				nome = 'Vidoza'
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'streamango.' in resultado['URL'].lower():
				nome = 'Streamango'
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'mixdrop.to' in resultado['URL'].lower():
				nome = 'Mixdrop'
				servidores.append(resultado['URL'])
				titulos.append('Servidor #%s: %s' % (i, nome))
		if resultado['URL2'] != '':
			i+=1
			if 'openload' in resultado['URL2'].lower():
				nome = "OpenLoad"
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidzi' in resultado['URL2'].lower():
				nome = 'Vidzi'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'google' in resultado['URL2'].lower() or 'cloud.mail.ru' in resultado['URL2'].lower():
				nome = 'MrPiracy'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'uptostream.com' in resultado['URL2'].lower():
				nome = 'UpToStream'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'rapidvideo.com' in resultado['URL2'].lower() or 'raptu' in resultado['URL2'].lower():
				nome = 'Raptu'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidoza.net' in resultado['URL2'].lower():
				nome = 'Vidoza'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'streamango.' in resultado['URL2'].lower():
				nome = 'Streamango'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'mixdrop.to' in resultado['URL2'].lower():
				nome = 'Mixdrop'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
		try:
			if resultado['URL3'] != '':
				i+=1
				if 'openload' in resultado['URL3'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL3'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL3'].lower() or 'cloud.mail.ru' in resultado['URL3'].lower():
					nome = 'MrPiracy'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL3'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL3'].lower() or 'raptu' in resultado['URL3'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL3'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL3'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.to' in resultado['URL3'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass
		try:
			if resultado['URL4'] != '':
				i+=1
				if 'openload' in resultado['URL4'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL4'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL4'].lower() or 'cloud.mail.ru' in resultado['URL4'].lower():
					nome = 'MrPiracy'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL4'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL4'].lower() or 'raptu' in resultado['URL4'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL4'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL4'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.to' in resultado['URL4'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		try:
			if resultado['URL5'] != '':
				i+=1
				if 'openload' in resultado['URL5'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL5'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL5'].lower() or 'cloud.mail.ru' in resultado['URL5'].lower():
					nome = 'MrPiracy'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL5'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL5'].lower() or 'raptu' in resultado['URL5'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL5'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL5'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.to' in resultado['URL5'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		try:
			if resultado['URL6'] != '':
				i+=1
				if 'openload' in resultado['URL6'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL8'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL6'].lower()or 'cloud.mail.ru' in resultado['URL6'].lower():
					nome = 'MrPiracy'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL8'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL6'].lower() or 'raptu' in resultado['URL6'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL6'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL6'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.to' in resultado['URL6'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		try:
			if resultado['URL7'] != '':
				i+=1
				if 'openload' in resultado['URL7'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL7'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL7'].lower()or 'cloud.mail.ru' in resultado['URL7'].lower():
					nome = 'MrPiracy'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL7'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL7'].lower() or 'raptu' in resultado['URL7'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL7'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL7'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.to' in resultado['URL7'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		legenda = ''

		"""for s in servidores:
			#controlo.log(s)
		for l in titulos:
			#controlo.log(l)"""

		if '://' in resultado['legenda'] or resultado['legenda'] == '':
			legenda = self.API+'subs/%s.srt' % resultado['IMBD']
		elif resultado['legenda'] != '' and resultado['legenda'] != 'semlegenda':
			if not '.srt' in resultado['legenda']:
				resultado['legenda'] = resultado['legenda']+'.srt'
			legenda = self.API+'subs/%s' % resultado['legenda']
		try:
			if resultado['semlegenda'] == "1":
				legenda = ''
		except:
			pass
		try:
			if resultado['legenda'] == "semlegenda":
				legenda = ''
		except:
			pass
		legendaAux = legenda
		ext_g = 'coiso'
		servidor = 0
		if controlo.addon.getSetting('melhor-fonte') == 'true':
			i = 0
			for nome in titulos:
				if 'MrPiracy' in nome:
					servidor = i
					break
				if 'OpenLoad' in nome:
					servidor = i
				i = i+1

		else:	
			if len(titulos) > 1:
				servidor = controlo.select('Escolha o servidor', titulos)
			else:
				servidor = 0

		if 'vidzi' in servidores[servidor]:
			vidzi = URLResolverMedia.Vidzi(servidores[servidor])
			stream = vidzi.getMediaUrl()
			legenda = vidzi.getSubtitle()
		elif 'uptostream.com' in servidores[servidor]:
			stream = URLResolverMedia.UpToStream(servidores[servidor]).getMediaUrl()
		elif 'server.mrpiracy.win' in servidores[servidor]:
			stream = servidores[servidor]
		elif 'openload' in servidores[servidor]:
			stream = URLResolverMedia.OpenLoad(servidores[servidor]).getMediaUrl()
			"""legenda = URLResolverMedia.OpenLoad(servidores[servidor]).getSubtitle()
			if not '.vtt' in legenda or legenda == '':
				legenda = legendaAux"""
		elif 'drive.google.com/' in servidores[servidor]:
			stream, ext_g = URLResolverMedia.GoogleVideo(servidores[servidor]).getMediaUrl()
		elif 'cloud.mail.ru' in servidores[servidor]:
			stream, ext_g = URLResolverMedia.CloudMailRu(servidores[servidor]).getMediaUrl()
		elif 'rapidvideo.com' in servidores[servidor] or 'raptu' in servidores[servidor]:
			rapid = URLResolverMedia.RapidVideo(servidores[servidor])
			stream = rapid.getMediaUrl()
			legenda = rapid.getLegenda()
		elif 'vidoza.net' in servidores[servidor]:
			vidoz = URLResolverMedia.Vidoza(servidores[servidor])
			stream = vidoz.getMediaUrl()
			legenda = vidoz.getLegenda()
		elif 'streamango.' in servidores[servidor]:
			streaman = URLResolverMedia.Streamango(servidores[servidor])
			stream = streaman.getMediaUrl()
			legenda = streaman.getLegenda()
		elif 'mixdrop.' in servidores[servidor]:
			mixdrop = URLResolverMedia.Mixdrop(servidores[servidor])
			stream = mixdrop.getMediaUrl()
			legenda = mixdrop.getLegenda()

		"""if coiso == 'filme':
			legenda = legendaAux
			if resultado['IMBD'] not in legenda:
				legenda = self.API+'subs/%s.srt' % resultado['IMBD']"""

		if legenda == '':
			legenda = legendaAux
		return stream, legenda, ext_g

	def pesquisa(self, url):
		vistos = Database.selectFilmes()
		qualidade = ''
		if 'filmes' in url:
			ficheiro = os.path.join(controlo.pastaDados,'filmes_pesquisa.mrpiracy')
			tipo = 0
			qualidade = definicoes.getQualidade()
		elif 'series' in url:
			ficheiro = os.path.join(controlo.pastaDados,'series_pesquisa.mrpiracy')
			tipo = 1
			qualidade = '2'
			site = 'series'
		elif 'animes' in url:
			ficheiro = os.path.join(controlo.pastaDados,'animes_pesquisa.mrpiracy')
			tipo = 2
			qualidade = '2'
			site = 'animes'

		if 'page' not in url:
			try:
				tipo = controlo.select(u'Onde quer pesquisar?', ['Filmes', 'Series', 'Animes'])
			except:
				return False
			teclado = controlo.teclado('', 'O que quer pesquisar?')
			if tipo == 0:
				url = self.API_SITE+'filmes.php?action=pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'filmes_pesquisa.mrpiracy')
				qualidade = definicoes.getQualidade()
			elif tipo == 1:
				url = self.API_SITE+'series.php?action=pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'series_pesquisa.mrpiracy')
				qualidade = '2'
				site = 'series'
			elif tipo == 2:
				url = self.API_SITE+'animes.php?action=pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'animes_pesquisa.mrpiracy')
				qualidade = '2'
				site = 'animes'
				
			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
				f.close()
				teclado.setDefault(texto)
			teclado.doModal()
			
			if teclado.isConfirmed():
				strPesquisa = teclado.getText()
				dados = urllib.urlencode({'texto': strPesquisa, 'qualidade': qualidade})
				try:
					f = open(ficheiro, mode="w")
					f.write(strPesquisa)
					f.close()
				except:
					traceback.print_exc()
					print "Não gravou o conteudo em %s" % ficheiro

				resultado = controlo.abrir_url(url,post=dados, header=controlo.headers, cookie=definicoes.getCookie())
		else:
			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
				f.close()
			dados = urllib.urlencode({'texto': texto, 'qualidade':qualidade})
			resultado = controlo.abrir_url(url,post=dados, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)

		try:
			if resultado['codigo'] == 204:
				controlo.alerta('MrPiracy', 'Deve Indicar um valor para pesquisa.')
			return False
		except:
			resultado = resultado

		opcao = controlo.addon.getSetting('marcarVisto')

		if resultado['data'] != '':
			if tipo == 0:
				for i in resultado['data']:
					self.setFilme(i, vistos, opcao)
			elif tipo == 1 or tipo == 2:
				for i in resultado['data']:
					self.setSeries(i, vistos, opcao, site)

			current = resultado['meta']['current']
			total = resultado['meta']['total']
			try: proximo = resultado['meta']['paginacao']['next']
			except: pass 
			if int(current) < int(total):
				controlo.addDir('Proxima pagina ('+str(current)+'/'+str(total)+')', proximo, 'pesquisa', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
			definicoes.vista_filmesSeries()
	def marcarVisto(self, url):
		
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		#controlo.log(url)
		resultado = json.loads(resultado)[0]
		
		links = url.split('/')
		opcao = controlo.addon.getSetting('marcarVisto')
		colocar = 0
		if 'filme' in url:
			id_video = resultado['id_video']
			imdb = resultado['IMBD']
			post = {'id_filme': id_video}
			url = self.API_SITE+'index.php?action=marcar-visto-filme&idFilme='+id_video
			tipo = 0
		elif 'serie' in url:
			
			imdb  = resultado['fotoSerie'].split('/')[-1].split('.')[0]
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_serie': id_video, 'temporada': temporada, 'episodio':episodio}
			url = (self.API_SITE+'index.php?action=marcar-visto-episodio&idSerie=%s&temporada=%s&episodio=%s' % (id_video, temporada, episodio) )
			tipo = 1
		elif 'anime' in url:
			imdb  = resultado['fotoSerie'].split('/')[-1].split('.')[0]
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_anime': id_video, 'temporada': temporada, 'episodio':episodio}
			url = (self.API_SITE+'index.php?action=marcar-visto-episodio&idSerie=%s&temporada=%s&episodio=%s' % (id_video, temporada, episodio) )
			tipo = 2
		#controlo.log(url)
		if opcao == '0' or opcao == '2': 
			pastaVisto=os.path.join(controlo.pastaDados,'vistos')
			try:
				os.makedirs(pastaVisto)
			except:
				pass

			if tipo == 1 or tipo == 2:
				ficheiro = os.path.join(pastaVisto, str(id_video)+'_S'+str(temporada)+'x'+str(episodio)+'.mrpiracy')
			elif tipo == 0:
				ficheiro = os.path.join(pastaVisto, str(id_video)+'.mrpiracy')


			if not os.path.exists(ficheiro):
				f = open(ficheiro, 'w')
				f.write('')
				f.close()
			colocar = 1
		if opcao == '1' or opcao == '2': 

			try:
				resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
				resultado = json.loads(resultado)
				if resultado['mensagem']['codigo'] == 200:
					colocar = 1
				if resultado['mensagem']['codigo'] == 201:
					colocar = 2
				elif resultado['mensagem']['codigo'] == 204:
					colocar = 3
				userVistos = resultado['userVistos']

				if userVistos != "" or userVistos != []:
					try:
						vistos_filmes = ','.join(ast.literal_eval(userVistos).values())
					except:
						vistos_filmes = str(0)
				else:
					vistos_filmes = str(0)
			

				if tipo == 0:
					controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'vistos_filmes.mrpiracy'), vistos_filmes)
				if tipo == 1 or tipo == 2:
					controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'vistos_series.mrpiracy'), vistos_filmes)
			except:
				colocar = 4
				pass
		if Trakt.loggedIn():
			if 'PT' in imdb:
				imdb = re.compile('(.+?)PT').findall(imdb)[0]
			if 'pt' in imdb:
				imdb = re.compile('(.+?)pt').findall(imdb)[0]
			if tipo == 2 or tipo == 1:
				if '/' in episodio:
					ep = episodio.split('/')
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[1])
				elif 'e' in episodio:
					ep = episodio.split('e')
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, ep[1])
				else:
					Trakt.markwatchedEpisodioTrakt(imdb, temporada, episodio)
			elif tipo == 0:
				Trakt.markwatchedFilmeTrakt(imdb)
			self.getTrakt()
		if colocar == 1:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		if colocar == 2:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como não visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		elif colocar == 3:
			controlo.alerta('MrPiracy', 'Ocorreu um erro ao marcar como visto')
		elif colocar == 4:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como visto no Trakt"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
	def marcarNaoVisto(self, url):

		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		
		resultado = json.loads(resultado)[0]
		links = url.split('/')
		opcao = controlo.addon.getSetting('marcarVisto')
		colocar = 0
		if 'filme' in url:
			id_video = resultado['id_video']
			imdb = resultado['IMBD']
			post = {'id_filme': id_video}
			url = self.API_SITE+'index.php?action=marcar-visto-filme&idFilme='+id_video
			tipo = 0
		elif 'serie' in url:
			imdb  = resultado['fotoSerie'].split('/')[-1].split('.')[0]
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_serie': id_video, 'temporada': temporada, 'episodio':episodio}
			url = (self.API_SITE+'index.php?action=marcar-visto-episodio&idSerie=%s&temporada=%s&episodio=%s' % (id_video, temporada, episodio) )
			tipo = 1
		elif 'anime' in url:
			imdb  = resultado['fotoSerie'].split('/')[-1].split('.')[0]
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			post = {'id_anime': id_video, 'temporada': temporada, 'episodio':episodio}
			url = (self.API_SITE+'index.php?action=marcar-visto-episodio&idSerie=%s&temporada=%s&episodio=%s' % (id_video, temporada, episodio) )
			tipo = 2
			
		if opcao == '0' or opcao == '2': 
			pastaVisto=os.path.join(controlo.pastaDados,'vistos')
			try:
				os.makedirs(pastaVisto)
			except:
				pass

			if tipo == 1 or tipo == 2:
				ficheiro = os.path.join(pastaVisto, str(id_video)+'_S'+str(temporada)+'x'+str(episodio)+'.mrpiracy')
			elif tipo == 0:
				ficheiro = os.path.join(pastaVisto, str(id_video)+'.mrpiracy')


			if os.path.exists(ficheiro):
				os.remove(ficheiro)
			colocar = 1
		if opcao == '1' or opcao == '2': 
			try:
				resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
				resultado = json.loads(resultado)
				if resultado['mensagem']['codigo'] == 200:
					colocar = 1
				if resultado['mensagem']['codigo'] == 201:
					colocar = 2
				elif resultado['mensagem']['codigo'] == 204:
					colocar = 3
				userVistos = resultado['userVistos']

				if userVistos != "" or userVistos != []:
					try:
						vistos = ','.join(ast.literal_eval(userVistos).values())
					except:
						vistos = str(0)
				else:
					vistos = str(0)
				if tipo == 0:
					controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'vistos_filmes.mrpiracy'), vistos)
				if tipo == 1 or tipo == 2:
					controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'vistos_series.mrpiracy'), vistos)
			except:
				colocar = 4
				pass		
		if Trakt.loggedIn():
			if 'PT' in imdb:
				imdb = re.compile('(.+?)PT').findall(imdb)[0]
			if 'pt' in imdb:
				imdb = re.compile('(.+?)pt').findall(imdb)[0]
			if tipo == 2 or tipo == 1:
				if '/' in episodio:
					ep = episodio.split('/')
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[1])
				elif 'e' in episodio:
					ep = episodio.split('e')
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[0])
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, ep[1])
				else:
					Trakt.marknotwatchedEpisodioTrakt(imdb, temporada, episodio)
			elif tipo == 0:
				Trakt.marknotwatchedFilmeTrakt(imdb)
			self.getTrakt()
		if colocar == 1:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		if colocar == 2:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como não visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		if colocar == 3:
			controlo.alerta('MrPiracy', 'Ocorreu um erro ao marcar como visto')
		elif colocar == 4:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como não visto no Trakt"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def download(self, url):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		links = url.split('/')
		
		if 'filme' in url:
			id_video = links[-1]
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['IMBD']
			tipo = 0
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			tipo = 1
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			imdb = resultado['imdbSerie']
			id_video = resultado['id_serie']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			tipo = 2

		

		resultado = controlo.abrir_url(url, header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		
		resultado = json.loads(resultado)
		legendasOn = False
		stream, legenda, ext_g = self.getStreamLegenda(resultado)
		
		folder = xbmc.translatePath(controlo.addon.getSetting('pastaDownloads'))
		if legenda != '':
			legendasOn = True
		if tipo > 0:
			if tipo == 1:
				resultadoa = controlo.abrir_url(self.API_SITE+'serie/'+str(id_video), header=controlo.headers)
			elif tipo == 2:
				resultadoa = controlo.abrir_url(self.API_SITE+'anime/'+str(id_video), header=controlo.headers)
			resultadoa = json.loads(resultadoa)
			if not xbmcvfs.exists(os.path.join(folder,'series')):
				xbmcvfs.mkdirs(os.path.join(folder,'series'))
			if not xbmcvfs.exists(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles']))):
				xbmcvfs.mkdirs(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles'])))
			if not xbmcvfs.exists(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles']),"Temporada "+str(temporada))):
				xbmcvfs.mkdirs(os.path.join(folder,'series',self.remove_accents(resultadoa['nome_ingles']),"Temporada "+str(temporada)))
			folder = os.path.join(folder, 'series', self.remove_accents(resultadoa['nome_ingles']), "Temporada "+str(temporada))
			name = "e"+str(episodio)+" - "+self.remove_accents(resultado['nome_episodio'])
		else:
			if not xbmcvfs.exists(os.path.join(folder,'filmes')):
				xbmcvfs.mkdirs(os.path.join(folder,'filmes'))
			folder = os.path.join(folder,'filmes')
			name = self.remove_accents(resultado['nome_ingles'])

	
		streamAux = self.clean(stream.split('/')[-1])
		extensaoStream = self.clean(streamAux.split('.')[-1])

		if '?mim' in extensaoStream:
			extensaoStream = re.compile('(.+?)\?mime=').findall(extensaoStream)[0]


		if ext_g != 'coiso':
			extensaoStream = ext_g

		extensaoStream = 'mp4'

		nomeStream = name+'.'+extensaoStream	

		Downloader.Downloader().download(os.path.join(folder.decode("utf-8"), nomeStream), stream, nomeStream)
		
		if legendasOn:
			legendaAux = self.clean(legenda.split('/')[-1])
			extensaoLegenda = self.clean(legendaAux.split('.')[1])
			nomeLegenda = name+'.'+extensaoLegenda
			self.download_legendas(legenda, os.path.join(folder, nomeLegenda))

	def download_legendas(self,url,path):
		contents = controlo.abrir_url(url, header=controlo.headers)
		if contents:
			fh = open(path, 'w')
			fh.write(contents)
			fh.close()
		return
	def clean(self, text):
		command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
		regex = re.compile("|".join(map(re.escape, command.keys())))
		return regex.sub(lambda mo: command[mo.group(0)], text)
	def progressoTrakt(self):

		vistos = Database.selectProgresso()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')

		for serie in json.loads(vistos):
			url = 'https://api-v2launch.trakt.tv/shows/%s/progress/watched?hidden=false&specials=false' % serie["show"]["ids"]["slug"]
			data = Trakt.getTrakt(url)
			if data == "asd":
				continue
			data = json.loads(data)
		
			try:
				episodioN = str(data["next_episode"]["number"])
				temporadaNumero = str(data["next_episode"]["season"])
			except:
				continue

			if serie["show"]["ids"]["imdb"] is None:
				continue

			
			url = self.API_SITE+'serie/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"],temporadaNumero, episodioN )
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultado = json.loads(resultado)
			except ValueError:
				continue
			if 'codigo' in resultado:
				url = self.API_SITE+'serie/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"]+'PT',temporadaNumero, episodioN )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"],temporadaNumero, episodioN )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"]+'PT',temporadaNumero, episodioN )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				continue
			url = self.API_SITE+'serie/%s' % (resultado['id_serie'])
			resultadoS = controlo.abrir_url(url, header=controlo.headers)
			if resultadoS == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultadoS = json.loads(resultadoS)
			except ValueError:
				continue
			if 'codigo' in resultadoS:
				url = self.API_SITE+'anime/%s' % (resultado['id_serie'])
				resultadoS = controlo.abrir_url(url, header=controlo.headers)
				if resultadoS == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultadoS = json.loads(resultadoS)
				except ValueError:
					continue
		

			if resultado['URL'] == '' and resultado['URL2'] == '':
				continue

			infoLabels = {'Title': resultado['nome_episodio'], 'Code': resultado['IMBD'], 'Episode': resultado['episodio'], 'Season': resultado['temporada'] }
			try:
				nome = resultado['nome_episodio'].decode('utf-8')
			except:
				nome = resultado['nome_episodio'].encode('utf-8')
			imagem = ''
			if resultado['imagem'] == "1":
				imagem = self.API+'images/series/'+resultado['IMBD']+'.jpg'
			elif resultado['imagem'] == "0":
				imagem = self.API+'images/capas/'+resultado['imdbSerie']+'.jpg'
			categoria = resultadoS['categoria1']
			if resultadoS['categoria2'] != '':
				categoria += ','+resultadoS['categoria2']
			if resultadoS['categoria3'] != '':
				categoria += ','+resultadoS['categoria3']
			pt = ''
			br = ''
			final = ''
			semLegenda = ''
			if resultado['fimtemporada'] == "1":
				final = '[B]Final da Temporada [/B]'
			if resultado['semlegenda'] == "1":
				semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if 'PT' in resultado['IMBD']:
				resultado['IMBD'] = re.compile('(.+?)PT').findall(resultado['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			controlo.addVideo(pt+br+semLegenda+final+'[B]'+resultado['nomeSerie']+'[/B] '+temporadaNumero+'x'+episodioN+' . '+nome, self.API_SITE+tipo+'/'+str(resultado['id_serie'])+'/temporada/'+str(resultado['temporada'])+'/episodio/'+str(resultado['episodio']), 'player', imagem, False, 'episodio', resultado['temporada'], resultado['episodio'], infoLabels, self.API+resultado['background'])
		definicoes.vista_filmesSeries()
		xbmc.executebuiltin("Container.SetViewMode(50)")
	def watchlistFilmes(self):
		vistos = Database.selectWatchFilmes()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		opcao = controlo.addon.getSetting('marcarVisto')
		for f in json.loads(vistos):
			if f["movie"]["ids"]["imdb"] is None:
				continue
			imdb = f["movie"]["ids"]["imdb"]
			url = self.API_SITE+'filme/%s/imdb/qualidade/%s' % (imdb, definicoes.getQualidade())
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			if 'codigo' in resultado:
				continue
			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']
			
			pt = ''
			br = ''
			semLegenda = ''
			if resultado['legenda'] == "semlegenda":
				semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'

			if 'PT' in resultado['IMBD']:
				resultado['IMBD'] = re.compile('(.+?)PT').findall(resultado['IMBD'])[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			visto = False
			if opcao == '1' or opcao == '2':
				if resultado['visto'] == 1:
					visto = True
			elif opcao == '0' or opcao == '2':
				visto = self.verificarVistoLocal(resultado['id_video'])
			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
			
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]

			if resultado['verdepois'] == 1:
				menuVerDepois = True
			else:
				menuVerDepois = False

			if resultado['favorito'] == 1:
				menuFavorito = True
			else:
				menuFavorito = False
			controlo.addVideo(pt+br+semLegenda+nome+' ('+resultado['ano']+')', self.API_SITE+'filme/'+str(resultado['id_video']), 'player', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.API+resultado['background'], trailer=resultado['trailer'], favorito=menuFavorito, agendado=menuVerDepois)
		definicoes.vista_filmesSeries()

	def watchlistSeries(self):
		vistos = Database.selectWatchSeries()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		for s in json.loads(vistos):
			if s["show"]["ids"]["imdb"] is None:
				continue
			imdb = s["show"]["ids"]["imdb"]
		
			
			url = self.API_SITE+'serie/%s/imdb' % (s["show"]["ids"]["imdb"] )
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultado = json.loads(resultado)
			except ValueError:
				continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/imdb' % (s["show"]["ids"]["imdb"] )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				continue
			

			categoria = resultado['categoria1']
			if resultado['categoria2'] != '':
				categoria += ','+resultado['categoria2']
			if resultado['categoria3'] != '':
				categoria += ','+resultado['categoria3']

			infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
		
			try:
				nome = resultado['nome_ingles'].decode('utf-8')
			except:
				nome = resultado['nome_ingles'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]
			if resultado['visto'] == 1:
				visto=True
			else:
				visto=False
			if resultado['verdepois'] == 1:
				menuVerDepois = True
			else:
				menuVerDepois = False

			if resultado['favorito'] == 1:
				menuFavorito = True
			else:
				menuFavorito = False
			controlo.addDir(nome+' ('+resultado['ano']+')', self.API_SITE+tipo+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels,poster=self.API+resultado['background'],visto=visto, menuO=True, favorito=menuFavorito, agendado=menuVerDepois)
		definicoes.vista_filmesSeries()
	def remove_accents(self, input_str):
		input_str = input_str.replace("/", "")
		nkfd_form = unicodedata.normalize('NFKD', unicode(self.clean(input_str)))
		return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

	def verificarVistoLocal(self, idVideo, temporada=None, episodio=None):
		pastaVisto=os.path.join(controlo.pastaDados,'vistos')

		if temporada and episodio:
			ficheiroVisto = os.path.join(pastaVisto,str(idVideo)+'_S'+str(temporada)+'x'+str(episodio)+'.mrpiracy')
		else:
			ficheiroVisto = os.path.join(pastaVisto,str(idVideo)+'.mrpiracy')

		if os.path.exists(ficheiroVisto):
			return True
		else:
			return False

	def adicionarFavoritos(self, url):
	
		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id_video']
			tipo = 0
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=adicionar&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id_video']
			tipo = 1
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=adicionar&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id_video']
			tipo = 2
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=adicionar&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)

		if resultado['favoritos'] != "" or resultado['favoritos'] != []:
			try:
				favoritos = ','.join(map(str, resultado['favoritos']))
			except:
				favoritos = str(0)
		else:
			favoritos = str(0)

		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'favoritos.mrpiracy'), favoritos)

		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+nome+": Adicionado aos Favoritos"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
	def removerFavoritos(self, url):
		
		links = url.split('/')
		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id_video']
			tipo = 0
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=remover&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id_video']
			tipo = 1
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=remover&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id_video']
			tipo = 2
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=remover&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)

		if resultado['favoritos'] != "" or resultado['favoritos'] != []:
			try:
				favoritos = ','.join(map(str, resultado['favoritos']))
			except:
				favoritos = str(0)
		else:
			favoritos = str(0)
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'favoritos.mrpiracy'), favoritos)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+nome+": Removido dos Favoritos"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def adicionarAgendar(self, url):

		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id_video']
			tipo = 0
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=adicionar&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id_video']
			tipo = 1
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=adicionar&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id_video']
			tipo = 2
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=adicionar&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if resultado['ver_depois'] != "" or resultado['ver_depois'] != []:
			try:
				ver_depois = ','.join(map(str, resultado['ver_depois']))
			except:
				ver_depois = str(0)
		else:
			ver_depois = str(0)
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.mrpiracy'), ver_depois)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+nome+": Agendado"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def removerAgendar(self, url):
		
		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id_video']
			tipo = 0
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=remover&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id_video']
			tipo = 1
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=remover&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id_video']
			tipo = 2
			nome = resultado['nome_ingles']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=remover&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if resultado['ver_depois'] != "" or resultado['ver_depois'] != []:
			try:
				ver_depois = ','.join(map(str, resultado['ver_depois']))
			except:
				ver_depois = str(0)
		else:
			ver_depois = str(0)
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.mrpiracy'), ver_depois)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+nome+": Removido dos Agendados"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def traktListas(self):
		url = 'https://api.trakt.tv/users/%s/lists' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		listas = Trakt.getTrakt(url, login=False)
		
		for s in json.loads(listas):
			controlo.addDir(s['name']+' ('+str(s['item_count'])+' items)', url+'/'+str(s['ids']['trakt'])+'/items', 'traktListasItems', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		
		definicoes.vista_menu()

	def traktListasItems(self, url):
		lista = Trakt.getTrakt(url, login=False)
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenMrpiracy')
		opcao = controlo.addon.getSetting('marcarVisto')
		for s in json.loads(lista):
			if s['type'] == 'movie':
				if s["movie"]["ids"]["imdb"] is None:
					continue
				imdb = s["movie"]["ids"]["imdb"]
				url = self.API_SITE+'filme/%s/imdb/qualidade/%s' % (imdb, definicoes.getQualidade())
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				resultado = json.loads(resultado)
				if 'codigo' in resultado:
					continue
				categoria = resultado['categoria1']
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']
				
				pt = ''
				br = ''
				semLegenda = ''
				if resultado['legenda'] == "semlegenda":
					semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'

				if 'PT' in resultado['IMBD']:
					resultado['IMBD'] = re.compile('(.+?)PT').findall(resultado['IMBD'])[0]
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				visto = False
				if opcao == '1' or opcao == '2':
					if resultado['visto'] == 1:
						visto = True
				elif opcao == '0' or opcao == '2':
					visto = self.verificarVistoLocal(resultado['id_video'])
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['IMBD'] }
				
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]
				if resultado['verdepois'] == 1:
					menuVerDepois = True
				else:
					menuVerDepois = False

				if resultado['favorito'] == 1:
					menuFavorito = True
				else:
					menuFavorito = False
				controlo.addVideo(pt+br+semLegenda+nome+' ('+resultado['ano']+')', self.API_SITE+'filme/'+str(resultado['id_video']), 'player', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.API+resultado['background'], trailer=resultado['trailer'], favorito=menuFavorito, agendado=menuVerDepois)
			elif s['type'] == 'show':
				if s["show"]["ids"]["imdb"] is None:
					continue
				imdb = s["show"]["ids"]["imdb"]
			
				
				url = self.API_SITE+'serie/%s/imdb' % (s["show"]["ids"]["imdb"] )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'serie'
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
				if 'codigo' in resultado:
					url = self.API_SITE+'anime/%s/imdb' % (s["show"]["ids"]["imdb"] )
					resultado = controlo.abrir_url(url, header=controlo.headers)
					if resultado == 'DNS':
						controlo.alerta('MrPiracy', 'Tem de alterar os DNS para poder usufruir do addon')
						return False
					tipo = 'anime'
					try:
						resultado = json.loads(resultado)
					except ValueError:
						continue
				if 'codigo' in resultado:
					continue
				

				categoria = resultado['categoria1']
				if resultado['categoria2'] != '':
					categoria += ','+resultado['categoria2']
				if resultado['categoria3'] != '':
					categoria += ','+resultado['categoria3']

				br = ''
				pt = ''
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if 'PT' in resultado['IMBD']:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				infoLabels = {'Title': resultado['nome_ingles'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['IMBD'] }
			
				try:
					nome = resultado['nome_ingles'].decode('utf-8')
				except:
					nome = resultado['nome_ingles'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]
				if resultado['visto'] == 1:
					visto=True
				else:
					visto=False
				if resultado['verdepois'] == 1:
					menuVerDepois = True
				else:
					menuVerDepois = False

				if resultado['favorito'] == 1:
					menuFavorito = True
				else:
					menuFavorito = False
				controlo.addDir(pt+br+nome+' ('+resultado['ano']+')', self.API_SITE+tipo+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels,poster=self.API+resultado['background'],visto=visto, menuO=True, favorito=menuFavorito, agendado=menuVerDepois)
		definicoes.vista_filmesSeries()

	def setFilme(self, i, vistos, opcao):
		categoria = definicoes.getCategoria(i['categoria1'])
		if int(i['categoria2']) != 0:
			categoria += ','+definicoes.getCategoria(i['categoria2'])
		if int(i['categoria3']) != 0:
			categoria += ','+definicoes.getCategoria(i['categoria3'])
		
		pt = ''
		br = ''
		semLegenda = ''
		if i['legenda'] == "semlegenda":
			semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
		if 'Brasileiro' in categoria:
			br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
		if 'Portu' in categoria:
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		cor = "white"
		if 'PT' in i['IMBD']:
			i['IMBD'] = re.compile('(.+?)PT').findall(i['IMBD'])[0]
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		visto = False
		vistoa = False
		if opcao == '1' or opcao == '2':
			if self.getVistoFilme(i['id_video']) == True:
				vistoa = True
		elif opcao == '0' or opcao == '2':
			vistoa = self.verificarVistoLocal(i['id_video'])
		
		if Trakt.loggedIn():
			for v in json.loads(vistos):
				if v["movie"]["ids"]["imdb"] is None:
					continue
				if v["movie"]["ids"]["imdb"] == i['IMBD']:
					visto = True
					cor = "blue"
					break
				else:
					visto = False
		if vistoa or visto:
			visto = True
		else:
			visto = False
		try:
			nome = i['nome_ingles'].decode('utf-8')
		except:
			nome = i['nome_ingles'].encode('utf-8')
		if 'http' not in i['foto']:
			i['foto'] = self.API+'images/capas/'+i['foto'].split('/')[-1]

		menuVerDepois = self.getVerDepois(i['id_video'])
		
		imdbR = json.loads(i['imdbRating'])
		
		menuFavorito = self.getFavoritos(i['id_video'])
		url = self.API_SITE+'filmes.php?action='+str(i['id_video'])
		infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot':i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': imdbR['trailer'], 'Director': i['diretor'], 'Rating': imdbR['ranking'], 'IMDBNumber': i['IMBD'] }
		controlo.addVideo('[COLOR '+cor+']'+pt+br+semLegenda+nome+' ('+i['ano']+')[/COLOR]', self.API_SITE+'filmes.php?action=id&idFilme='+str(i['id_video']), 'player', i['foto'],visto, 'filme', 0, 0, infoLabels, self.API+i['background'], trailer=imdbR['trailer'], favorito=menuFavorito, agendado=menuVerDepois)

	def setSeries(self, i, vistos, opcao, tipo):
		categoria = definicoes.getCategoria(i['categoria1'])
		if int(i['categoria2']) != 0:
			categoria += ','+definicoes.getCategoria(i['categoria2'])
		if int(i['categoria3']) != 0:
			categoria += ','+definicoes.getCategoria(i['categoria3'])
		br = ''
		pt = ''
		if 'Brasileiro' in categoria:
			br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
		if 'Portu' in categoria:
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		if 'PT' in i['IMBD']:
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		visto = False
		vistoa = False
		if opcao == '1' or opcao == '2':
			if self.getVistoFilme(i['id_video']) == True:
				vistoa = True
		elif opcao == '0' or opcao == '2':
			vistoa = self.verificarVistoLocal(i['id_video'])
		if vistoa:
			visto = True
		else:
			visto = False
		try:
			nome = i['nome_ingles'].decode('utf-8')
		except:
			nome = i['nome_ingles'].encode('utf-8')
		if 'http' not in i['foto']:
			i['foto'] = self.API+'images/capas/'+i['foto'].split('/')[-1]
		
		menuVerDepois = self.getVerDepois(i['id_video'])
		imdbR = json.loads(i['imdbRating'])
		menuFavorito = self.getFavoritos(i['id_video'])
		
		infoLabels = {'Title': i['nome_ingles'], 'Year': i['ano'], 'Genre': categoria, 'Plot': i['descricao_video'], 'Cast':i['atores'].split(','), 'Trailer': imdbR['trailer'], 'Director': i['diretor'], 'Rating': imdbR['ranking'], 'Code': i['IMBD'] }
		controlo.addDir(pt+br+nome+' ('+i['ano']+')', self.API_SITE+tipo+'.php?action=id&idSerie='+str(i['id_video']), 'temporadas', i['foto'], tipo='serie', infoLabels=infoLabels,poster=self.API+i['background'],visto=visto, menuO=True, favorito=menuFavorito, agendado=menuVerDepois)

