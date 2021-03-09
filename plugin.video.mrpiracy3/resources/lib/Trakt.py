# -*- coding: utf-8 -*-

import os, xbmcgui, xbmc,xbmcvfs,xbmcaddon,time, urllib, re, sys, traceback, base64, pprint, zipfile
from . import controlo, Database, utils, client

try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import six
from six.moves import urllib_parse

import simplejson as json

try:  # Python 2
    from urlparse import urlparse, urljoin
    from urllib import quote, urlencode, quote_plus, addinfourl
    import cookielib
    import urllib2
    from cStringIO import StringIO
    from HTMLParser import HTMLParser
    unescape = HTMLParser().unescape
    HTTPError = urllib2.HTTPError
except ImportError:  # Python 3
    from http import cookiejar as cookielib
    from html import unescape
    import urllib.request as urllib2
    from io import StringIO
    from urllib.parse import urlparse, urljoin, quote, urlencode, quote_plus
    from urllib.response import addinfourl
    from urllib.error import HTTPError
finally:
    urlopen = urllib2.urlopen
    Request = urllib2.Request

import sys
if sys.version_info[0] >= 3:
    bytes = bytes
    str = unicode = basestring = str



encoding = 'utf-8'

__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo("id")
__ADDON__   = xbmcaddon.Addon(__ADDON_ID__)
__TRAKT_API__ = 'https://api.trakt.tv'
__TRAKT_CLIENT__ = 'bad109e8a649b37981b17acb5f8b42ddca1e00d149a265bd2b51ac3a873ce988'
__TRAKT_SECRET__ = '86848761842c739716c7c0a1bae42c4a4b46778860f6b86d7c1e91416cb1e6f4'
__TRAKT_REDIRECT__ = 'urn:ietf:wg:oauth:2.0:oob'

__TVDB_APIKEY__ = 'MUI0QThDRDFCMTQwNEY0Qg=='

__HEADERS_TRAKT__ = {'Content-Type': 'application/json', 'trakt-api-key': __TRAKT_CLIENT__, 'trakt-api-version': '2'}
__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def client(url, post=None, headers=None, as_bytes=False):
    if isinstance(post, dict):
        post = bytes(urlencode(post), encoding='utf-8')
    elif isinstance(post, str) and sys.version_info[0] >= 3:
        post = bytes(post, encoding='utf-8')

    req = urllib2.Request(url, data=post, headers=headers)
    response = urllib2.urlopen(req)
    content = response.headers
    result = response.read()
    response.close()
    if not as_bytes:
        result = six.ensure_text(result, errors='ignore')
    return result, headers, content

def getTraktCredentialsInfo():
    user = controlo.definicoes('utilizadorTrakt').strip()
    token = controlo.definicoes('tokenTrakt')
    refresh = controlo.definicoes('refreshTrakt')

    if (user == '' or token == '' or refresh == ''):
        return False
    return True

def getTraktAsJson(url, post=None):
    try:
    
        r, res_headers = getTrakt(url, post)


        r = utils.json_loads_as_str(r)

        if 'X-Sort-By' in res_headers and 'X-Sort-How' in res_headers:
            r = sort_list(res_headers['X-Sort-By'], res_headers['X-Sort-How'], r)
        return r
    except Exception:
        pass

def getTrakt(url, post=None):
    try:
        url = urllib_parse.urljoin(__TRAKT_API__, url)
        url = url.encode().decode()
        post = json.dumps(post) if post else None

        if getTraktCredentialsInfo():
            __HEADERS_TRAKT__.update({'Authorization': 'Bearer %s' % controlo.definicoes('tokenTrakt')})

        result = client(url, post, __HEADERS_TRAKT__)
        resultado, resp_code, resp_header = utils.byteify(result)

        resultado = utils.byteify(resultado)

        total = len(resultado)


        if resp_code in ['500', '502', '503', '504', '520', '521', '522', '524']:
            controlo.log('Temporary Trakt Error: %s' % resp_code)
            return
        elif resp_code in ['404']:
            controlo.log('Object Not Found: %s' % resp_code)
            return        
        if resp_code not in ['401', '405']:
            return resultado, resp_header

        oauth = urllib_parse.urljoin(__TRAKT_API__, '/oauth/token')
        opost = {'client_id': __TRAKT_CLIENT__, 'client_secret': __TRAKT_SECRET__, 'redirect_uri': __TRAKT_REDIRECT__, 'grant_type': 'refresh_token', 'refresh_token': controlo.definicoes('refreshTrakt')}

        result = client(oauth, json.dumps(opost), __HEADERS_TRAKT__)
        resultado, resp_code, resp_header = utils.byteify(result)
        resultado = utils.json_loads_as_str(resultado)

        token, refresh = resultado['access_token'], resultado['refresh_token']

        controlo.setSetting(id='tokenTrakt', value=token)
        controlo.setSetting(id='refreshTrakt', value=refresh)

        __HEADERS_TRAKT__['Authorization'] = 'Bearer %S' % token

        result = client(url, post, __HEADERS_TRAKT__)
        resultado, resp_code, resp_header = utils.byteify(result)
        resultado = utils.byteify(resultado)
        return resultado, resp_header
    except Exception as e:
        traceException = traceback.format_exc()
        controlo.log('Trakt - Exception:\n' + str(traceException))
        controlo.log('Unknown Trakt Error: %s' % e)
        pass

def authTrakt():
    try:
        if getTraktCredentialsInfo():
            if controlo.yesnoDialog('Conta de Trakt já existe!', 'Deseja apagar?', '', 'MrPiracy Trakt'):
                controlo.setSetting(id='utilizadorTrakt', value='')
                controlo.setSetting(id='tokenTrakt', value='')
                controlo.setSetting(id='refreshTrakt', value='')
            raise Exception()

        post = {'client_id':__TRAKT_CLIENT__}

        resultado = getTraktAsJson('/oauth/device/code', post=post)
        verification_url = '1) Visite : [COLOR skyblue]%s[/COLOR]' % resultado['verification_url']
        user_code = six.ensure_text('2) Quando solicitado, introduza : [COLOR skyblue]%s[/COLOR]' % resultado['user_code'])
        expires_in = int(resultado['expires_in'])
        #expires_in = int(str(expires_in)[:2]) * 2
        device_code = resultado['device_code']
        interval = resultado['interval']

        progressDialog = controlo.progressDialog
        progressDialog.create('Trakt', verification_url + '[CR]' +  user_code)
        r = []

        for i in range(0, expires_in):
            try:
                percent = int(100 * float(i) / int(expires_in))
                progressDialog.update(max(1, percent), verification_url + '[CR]' + user_code)
                if progressDialog.iscanceled():
                    break
                time.sleep(1)
                if not float(i) % interval == 0:
                    raise Exception()
                r = getTraktAsJson('/oauth/device/token', {'client_id': __TRAKT_CLIENT__, 'client_secret': __TRAKT_SECRET__, 'code': device_code})
                if 'access_token' in r:
                    break
            except Exception:
                pass

        try:
            progressDialog.close()
        except Exception:
            pass

        
        token, refresh = r['access_token'], r['refresh_token']

        headers = {'Content-Type': 'application/json', 'trakt-api-key': __TRAKT_CLIENT__,
                   'trakt-api-version': 2, 'Authorization': 'Bearer %s' % token}


        resultado, resp, content = client(urllib_parse.urljoin(__TRAKT_API__, '/users/me'), headers=headers)
        controlo.log(resultado)
        resultado = utils.json_loads_as_str(resultado)

        user = resultado['username']

        controlo.setSetting(id='utilizadorTrakt', value=user)
        controlo.setSetting(id='tokenTrakt', value=token)
        controlo.setSetting(id='refreshTrakt', value=refresh)
        raise Exception()
    except Exception:
        controlo.openSettings('1.1')


def traktAuth():
    try:
        if not (__ADDON__.getSetting('utilizadorTrakt') == '' or __ADDON__.getSetting('tokenTrakt') == '' or __ADDON__.getSetting('refreshTrakt') == ''):
            dialog = xbmcgui.Dialog().yesno('MrPiracy.win', u'Conta de Trakt já existe!', '', 'Deseja apagar?', u'Não', 'Sim')
            if dialog:
                __ADDON__.setSetting('utilizadorTrakt', '')
                __ADDON__.setSetting('tokenTrakt', '')
                __ADDON__.setSetting('refreshTrakt', '')
            raise Exception()

        if __ADDON__.getSetting('utilizadorTrakt') == '' or __ADDON__.getSetting('tokenTrakt') == '' or __ADDON__.getSetting('refreshTrakt') == '':
            dialog = xbmcgui.Dialog().yesno('MrPiracy.win', u'1. Entrar: [COLOR blue]http://trakt.tv/pin/8928[/COLOR]', '2. Se pedido, autorizar o acesso da conta.', '3. Colocar o PIN.', 'Inserir PIN', 'Cancelar')

            if dialog:
                raise Exception()
            else:
                teclado = xbmc.Keyboard('', 'Inserir PIN')
                teclado.doModal()

                if teclado.isConfirmed():
                    pin = teclado.getText()

                    if pin == '' or pin == None:
                        raise Exception()


                    post = {'client_id': __TRAKT_CLIENT__, 'client_secret': __TRAKT_SECRET__, 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'authorization_code', 'code': pin}

                    resultado = controlo.abrir_url(__TRAKT_API__+'/oauth/token', post=json.dumps(post), header=__HEADERS_TRAKT__)
                    resultado = utils.json_loads_as_str(resultado)

                    token = resultado['access_token']
                    refresh = resultado['refresh_token']

                    __HEADERS_TRAKT__['Authorization'] = 'Bearer %s' % token

                    resultado = controlo.abrir_url(__TRAKT_API__+'/users/me', header=__HEADERS_TRAKT__)
                    resultado = utils.json_loads_as_str(resultado)

                    utilizador = resultado['username']

                    __ADDON__.setSetting('utilizadorTrakt', utilizador)
                    __ADDON__.setSetting('tokenTrakt', token)
                    __ADDON__.setSetting('refreshTrakt', refresh)
                else:
                    raise Exception()
    except:
        __ADDON__.openSettings()

def loggedIn():
    if not (controlo.definicoes('utilizadorTrakt').strip() == '' or controlo.definicoes('tokenTrakt') == '' or controlo.definicoes('refreshTrakt') == ''):
        return True
    else:
        return False

def getTrakt_OLD(url, post=None, login=True):
    try:
        if not post == None:
            post = json.dumps(post)

        if __ADDON__.getSetting('utilizadorTrakt') == '' or __ADDON__.getSetting('tokenTrakt') == '' or __ADDON__.getSetting('refreshTrakt') == '':
            return controlo.abrir_url(url, post=post, header=__HEADERS_TRAKT__)


        __HEADERS_TRAKT__['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenTrakt')



        link = __TRAKT_API__+url

        codigo, conteudo = controlo.abrir_url(url, post=post, header=__HEADERS_TRAKT__, code=True, erro=True)

        if codigo != '405' and codigo != '401':
            return conteudo

        tokenPost = {'client_id': __TRAKT_CLIENT__, 'client_secret': __TRAKT_SECRET__, 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'refresh_token', 'refresh_token': __ADDON__.getSetting('refreshTrakt')}
        #print "~~~~~~~~~~~~~~~~~ Trakt MrPiracy"
        #pprint.pprint(tokenPost)

        __HEADERS_TRAKT_v2__ = {'Content-Type': 'application/json', 'trakt-api-key': __TRAKT_CLIENT__, 'trakt-api-version': '2'}

        resultado = controlo.abrir_url(__TRAKT_API__+'/oauth/token', post=json.dumps(tokenPost), header=__HEADERS_TRAKT_v2__)
        resultado = utils.json_loads_as_str(resultado)


        #pprint.pprint(resultado)

        token = resultado['access_token']
        refresh = resultado['refresh_token']

        __ADDON__.setSetting('tokenTrakt', token)
        __ADDON__.setSetting('refreshTrakt', refresh)

        __HEADERS_TRAKT__['Authorization'] = 'Bearer %s' % token

        resultado = controlo.abrir_url(link, post=post, header=__HEADERS_TRAKT__)

        return resultado

    except:
        pass


def sort_list(sort_key, sort_direction, list_data):
    reverse = False if sort_direction == 'asc' else True
    if sort_key == 'rank':
        return sorted(list_data, key=lambda x: x['rank'], reverse=reverse)
    elif sort_key == 'added':
        return sorted(list_data, key=lambda x: x['listed_at'], reverse=reverse)
    elif sort_key == 'title':
        return sorted(list_data, key=lambda x: utils.title_key(x[x['type']].get('title')), reverse=reverse)
    elif sort_key == 'released':
        return sorted(list_data, key=lambda x: _released_key(x[x['type']]), reverse=reverse)
    elif sort_key == 'runtime':
        return sorted(list_data, key=lambda x: x[x['type']].get('runtime', 0), reverse=reverse)
    elif sort_key == 'popularity':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    elif sort_key == 'percentage':
        return sorted(list_data, key=lambda x: x[x['type']].get('rating', 0), reverse=reverse)
    elif sort_key == 'votes':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    else:
        return list_data

def getFilme(idIMDB, categoria):
    url = 'http://api-v2launch.trakt.tv/movies/%s?extended=full,images' % idIMDB
    urlpt = 'http://api-v2launch.trakt.tv/movies/%s/translations/pt' % idIMDB

    resultado = controlo.abrir_url(url, header=__HEADERS_TRAKT__)
    resultado = utils.json_loads_as_str(resultado)

    resultadopt = controlo.abrir_url(urlpt, header=__HEADERS_TRAKT__)
    resultadopt = utils.json_loads_as_str(resultadopt)

    if resultado["trailer"] is None:
        trailer = '-'
    else:
        trailer = resultado["trailer"]

    try:
        plot = resultadopt[0]["overview"]
    except:
        plot = resultado["overview"]

    if resultado["year"] is None:
        ano = "-"
    else:
        ano = str(resultado["year"])

    if resultado["images"]["poster"]["full"] is None:
        url2 = 'http://www.omdbapi.com/?i=%s&plot=full&r=json' % idIMDB
        resultado2 = controlo.abrir_url(url2, header=__HEADERS__)
        resultado2 = utils.json_loads_as_str(resultado2)

        poster = resultado2["Poster"]
    else:
        poster = resultado["images"]["poster"]["full"]

    if resultado["images"]["fanart"]["full"] is None:
        url2 = 'http://www.omdbapi.com/?i=%s&plot=full&r=json' % idIMDB
        resultado2 = controlo.abrir_url(url2, header=__HEADERS__)
        resultado2 = utils.json_loads_as_str(resultado2)

        fanart = resultado2["Poster"]
    else:
        fanart = resultado["images"]["fanart"]["full"]

    traktid = resultado["ids"]["trakt"]
    slug = resultado["ids"]["slug"]


    Database.insertFilmeDB(nome=resultado["title"], plot=plot, traktid=traktid, imdb=idIMDB, poster=poster, fanart=fanart, trailer=trailer, ano=ano, categoria=categoria, slug=slug)

    data = {}
    data["nome"] = resultado["title"]
    data["plot"] = plot
    data["imdb"] = idIMDB
    data["poster"] = poster
    data["fanart"] = fanart
    data["trailer"] = trailer
    data["ano"] = ano
    data["categoria"] = categoria
    return json.dumps(data)

def getSerie(idIMDB, categoria=None, slug=None):
    if idIMDB == 'tt3830558':
        slug = 'versailles'

    if slug:
        url = 'https://api-v2launch.trakt.tv/shows/%s?extended=full,images' % slug
    else:
        url = 'https://api-v2launch.trakt.tv/shows/%s?extended=full,images' % idIMDB
    #urlpt = 'https://api-v2launch.trakt.tv/shows/%s/translations/pt' % idIMDB

    resultado = controlo.abrir_url(url, header=__HEADERS_TRAKT__)
    resultado = utils.json_loads_as_str(resultado)

    if idIMDB == 'tt3830558':
        tvdbSerie = '300280'
    else:
        tvdbSerie = resultado["ids"]["tvdb"]

    urlTVDB = 'http://thetvdb.com/api/%s/series/%s/all/pt.zip' % (__TVDB_APIKEY__, tvdbSerie)

    resultadopt = controlo.abrir_url(urlTVDB)

    ficheiro = zipfile.ZipFile(StringIO.StringIO(resultadopt))
    resultadopt = ficheiro.read('pt.xml')
    ficheiro.close()

    soup = BeautifulSoup(resultadopt)
    if categoria is None:
        categoria = ''

    try:
        cat = soup.genre.text.split('|')
        categoria = ", ".join(cat)
        """i = 0
        categoria = ''
        for c in cat:
            if i == 0:
                categoria = c
            else:
                categoria = categoria +', '+ c
            i=i+1"""
    except:
        categoria = ''

    try:
        act = soup.actors.text.split('|')
        actores = ", ".join(act)
    except:
        actores = ''

    plot = soup.series.overview.text

    if resultado["images"]["poster"]["full"] is None:
        poster = "http://thetvdb.com/banners/"+soup.series.poster.text
    else:
        poster = resultado["images"]["poster"]["full"]

    if resultado["images"]["fanart"]["full"] is None:
        fanart = "http://thetvdb.com/banners/"+soup.series.fanart.text
    else:
        fanart = resultado["images"]["fanart"]["full"]

    """try:
        poster = 'http://thetvdb.com/banners/'+soup.filename.text
    except:
        poster = resultado["images"]["poster"]["full"]
    try:
        fanart = resultado["images"]["fanart"]["full"]
    except:
        fanart = 'http://thetvdb.com/banners/'+soup.filename.text
    """
    nomeSerie = resultado['title']

    airedSerie = soup.series.firstaired.text
    try:
        anoSerie = soup.series.firstaired.text.split('-')[0]
    except:
        anoSerie = ''

    traktid = resultado["ids"]["trakt"]
    slug = resultado["ids"]["slug"]

    Database.insertSerie(nomeSerie, plot, idIMDB, tvdbSerie, poster, fanart, airedSerie, anoSerie, traktid, slug, categoria=categoria, actores=actores)

    for serie in soup.findAll('episode'):
        if not (serie.seasonnumber.text == '0'):
            nomeEpisodio = serie.episodename.text
            plotEpisodio = serie.overview.text
            tvdbEpisodio = serie.id.text
            airedEpisodio = serie.firstaired.text
            temporadaEpisodio = serie.seasonnumber.text
            episodioEpisodio = serie.episodenumber.text
            posterEpisodio = "http://thetvdb.com/banners/"+serie.filename.text

            Database.insertEpisodio(nomeEpisodio, plotEpisodio, idIMDB, tvdbEpisodio, temporadaEpisodio, episodioEpisodio, fanart, posterEpisodio, airedEpisodio, nomeSerie, traktid, categoria=categoria, actores=actores)

    data = {}
    data["nome"] = nomeSerie
    data["plot"] = plot
    data["imdb"] = idIMDB
    data["poster"] = poster
    data["fanart"] = fanart
    data["aired"] = airedSerie
    data["categoria"] = categoria
    data["ano"] = anoSerie
    data["actores"] = actores
    return json.dumps(data)


def getTVDBByEpSe(idIMDB, temporada, episodio, slug=None):
    if slug:
        url = 'https://api-v2launch.trakt.tv/shows/%s?extended=full,images' % slug
    else:
        url = 'https://api-v2launch.trakt.tv/shows/%s?extended=full,images' % idIMDB

    resultado = controlo.abrir_url(url, header=__HEADERS_TRAKT__)
    resultado = utils.json_loads_as_str(resultado)

    if idIMDB == 'tt3830558':
        idTVDB = '300280'
    else:
        idTVDB = resultado["ids"]["tvdb"]

    serieNome = resultado['title']
    traktid = resultado["ids"]["trakt"]
    data = {}
    url = 'http://thetvdb.com/api/%s/series/%s/default/%s/%s/pt.xml' % (__TVDB_APIKEY__, idTVDB, temporada, episodio)

    soup = BeautifulSoup(controlo.abrir_url(url, header=__HEADERS__))


    try:
        cat = soup.genre.text.split('|')
        categoria = ", ".join(cat)
    except:
        categoria = ''

    try:
        act = soup.actors.text.split('|')
        actores = ", ".join(act)
    except:
        actores = ''

    try:
        data['poster'] = 'http://thetvdb.com/banners/'+soup.filename.text
    except:
        data['poster'] = resultado["images"]["poster"]["full"]
    """if resultado["images"]["poster"]["full"] is None:
        data['poster'] = 'http://thetvdb.com/banners/'+soup.filename.text
    else:
        data['poster'] = resultado["images"]["poster"]["full"]
"""
    try:
        data['fanart'] = resultado["images"]["fanart"]["full"]
    except:
        data['fanart'] = 'http://thetvdb.com/banners/'+soup.filename.text
    """if resultado["images"]["fanart"]["full"] is None:
        data['fanart'] = 'http://thetvdb.com/banners/'+soup.filename.text
    else:
        data['fanart'] = resultado["images"]["fanart"]["full"]
"""
    #Database.insertEpisodio(soup.episodename.text, soup.overview.text, idIMDB, idTVDB, temporada, episodio, data['fanart'], data['poster'], soup.firstaired.text, serieNome, traktid, categoria=categoria, actores=actores)

    data['serie'] = serieNome
    try:
        data['name'] = soup.episodename.text
    except:
        data['name'] = ''
    try:
        data['plot'] = soup.overview.text
    except:
        data['plot'] = ''
    try:
        data['actors'] = soup.gueststars.text
    except:
        data['actors'] = ''
    try:
        data['aired'] = soup.firstaired.text
    except:
        data['aired'] = ''
    try:
        data['director'] = soup.director.text
    except:
        data['director'] = ''
    try:
        data['writer'] = soup.writer.text
    except:
        data['writer'] = ''
    data['season'] = temporada
    data['episode'] = episodio
    data['tvdb'] = idTVDB
    data['imdb'] = idIMDB
    data['traktid'] = traktid
    json_data = json.dumps(data)

    return json_data

def markwatchedFilmeTrakt(imdb):
    if not imdb.startswith('tt'): imdb = 'tt' + imdb
    return getTrakt(__TRAKT_API__+'/sync/history', post={"movies": [{"ids": {"imdb": imdb}}]})


def marknotwatchedFilmeTrakt(imdb):
    if not imdb.startswith('tt'): imdb = 'tt' + imdb
    return getTrakt(__TRAKT_API__+'/sync/history/remove', post={"movies": [{"ids": {"imdb": imdb}}]})

def markwatchedEpisodioTrakt(imdb, temporada, episodio):
    #temporada, episodio = int('%01d' % int(temporada)), int('%01d' % int(episodio))
    #tvdb = Database.selectTVDBEpisodioDB(imdb, temporada, episodio)
    #return getTrakt('/sync/history', post={"shows": [{"seasons": [{"episodes": [{"number": episodio}], "number": temporada}], "ids": {"tvdb": tvdb}}]})
    #coiso =  getTrakt(__TRAKT_API__+'/sync/history', post={ "episodes": [ { "ids": { "tvdb": int(tvdb[0]) } } ] })
    if not imdb.startswith('tt'): imdb = 'tt' + imdb

    post = {"shows": [{"ids": {"imdb": imdb},"seasons": [{"number": int(temporada),"episodes": [{"number": int(episodio)}]}]}]}
    coiso = getTrakt(__TRAKT_API__+'/sync/history', post=post)

def marknotwatchedEpisodioTrakt(imdb, temporada, episodio):
    #temporada, episodio = int('%01d' % int(temporada)), int('%01d' % int(episodio))
    #tvdb = Database.selectTVDBEpisodioDB(imdb, temporada, episodio)
    #{"episodes": [{"ids": {"tvdb": tvdb[0]}}]}
    #return getTrakt('/sync/history/remove', post={"shows": [{"seasons": [{"episodes": [{"number": episodio}], "number": temporada}], "ids": {"tvdb": tvdb}}]})
    if not imdb.startswith('tt'): imdb = 'tt' + imdb
    post = {"shows": [{"ids": {"imdb": imdb},"seasons": [{"number": int(temporada),"episodes": [{"number": int(episodio)}]}]}]}
    coiso =  getTrakt(__TRAKT_API__+'/sync/history/remove', post=post)

def checkInFilmeTrakt(imdb):
    if not imdb.startswith('tt'): imdb = 'tt' + imdb
    return getTrakt(__TRAKT_API__+'/checkin', post={"movies": [{"ids": {"imdb": imdb}}]}, login=True)
def checkInEpisodioTrakt(imdb, temporada, episodio):
    if not imdb.startswith('tt'): imdb = 'tt' + imdb

    post = {"shows": [{"ids": {"imdb": imdb},"seasons": [{"number": int(temporada),"episodes": [{"number": int(episodio)}]}]}]}
    coiso = getTrakt(__TRAKT_API__+'/checkin', post=post)

def checkOutTrakt():
    return ''
    """
    req = urllib2.Request(__TRAKT_API__+'/checkin', headers=__HEADERS__)
    req.get_method = lambda: 'DELETE'
    erro = False
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as response:
        if erro == True:
            return str(response.code), "asd"

    link=response.read()

    response.close()
    return link"""

