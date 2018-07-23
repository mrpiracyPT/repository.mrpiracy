#!/usr/bin/python
# coding=utf-8

import urlparse,sys,xbmcplugin

from resources.lib import mrpiracy, controlo

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

try: modo = params.get('modo')
except: pass
try: url = params.get('url')
except: pass
try: iconimage = params.get('iconimage')
except: pass
try: nome = params.get('nome')
except: pass



if modo == None or modo == 'inicio':
	mrpiracy.mrpiracy().menu()
elif modo == 'menuFilmes':
	mrpiracy.mrpiracy().menuFilmes()
elif modo == 'menuSeries':
	mrpiracy.mrpiracy().menuSeries()
elif modo == 'menuAnimes':
	mrpiracy.mrpiracy().menuAnimes()
elif modo == 'filmes':
	mrpiracy.mrpiracy().filmes(url)
elif modo == 'series':
	mrpiracy.mrpiracy().series(url)
elif modo == 'animes':
	mrpiracy.mrpiracy().series(url)
elif modo == 'temporadas':
	mrpiracy.mrpiracy().temporadas(url)
elif modo == 'episodios':
	mrpiracy.mrpiracy().episodios(url)
elif modo == 'pesquisa':
	mrpiracy.mrpiracy().pesquisa(url)
elif modo == 'listagemAnos':
	mrpiracy.mrpiracy().listagemAnos(url)
elif modo == 'anos':
	mrpiracy.mrpiracy().anos(url)
elif modo == 'listagemGeneros':
	mrpiracy.mrpiracy().listagemGeneros(url)
elif modo == 'categorias':
	mrpiracy.mrpiracy().categorias(url)
elif modo == 'conta':
	mrpiracy.mrpiracy().conta()
elif modo == 'favoritos':
	mrpiracy.mrpiracy().favoritos(url)
elif modo == 'favoritosMenu':
	mrpiracy.mrpiracy().favoritosMenu()
elif modo == 'verdepois':
	mrpiracy.mrpiracy().verdepois(url)
elif modo == 'verdepoisMenu':
	mrpiracy.mrpiracy().verdepoisMenu()
elif modo == 'adicionar-favoritos':
	mrpiracy.mrpiracy().adicionarFavoritos(url)
elif modo == 'remover-favoritos':
	mrpiracy.mrpiracy().removerFavoritos(url)
elif modo == 'adicionar-agendar':
	mrpiracy.mrpiracy().adicionarAgendar(url)
elif modo == 'remover-agendar':
	mrpiracy.mrpiracy().removerAgendar(url)
elif modo == 'notificacoes':
	mrpiracy.mrpiracy().notificacoes(url)
elif modo == 'mensagens':
	mrpiracy.mrpiracy().mensagens(url)
elif modo == 'definicoes':
	mrpiracy.mrpiracy().definicoes()
elif modo == 'player':
	mrpiracy.mrpiracy().player(url)
elif modo == 'marcar-visto':
	mrpiracy.mrpiracy().marcarVisto(url)
elif modo == 'marcar-n-visto':
	mrpiracy.mrpiracy().marcarNaoVisto(url)
elif modo == 'download':
	mrpiracy.mrpiracy().download(url)
elif modo == 'menuTrakt':
	mrpiracy.mrpiracy().menuTrakt()
elif modo == 'traktWatchlistFilmes':
	mrpiracy.mrpiracy().watchlistFilmes()
elif modo == 'traktWatchlistSeries':
	mrpiracy.mrpiracy().watchlistSeries()
elif modo == 'progressoTrakt':
	mrpiracy.mrpiracy().progressoTrakt()
elif modo == 'loginTrakt':
	mrpiracy.mrpiracy().loginTrakt()
elif modo == 'traktListas':
	mrpiracy.mrpiracy().traktListas()
elif modo == 'traktListasItems':
	mrpiracy.mrpiracy().traktListasItems(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))