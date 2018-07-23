#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import xbmcgui
import xbmc
import xbmcvfs
import xbmcaddon
import time
import urllib
import urllib2
import re
import sys
import traceback
import json
import base64
import pprint
import zipfile
import StringIO
import Database
from t0mm0.common.net import Net

import controlo

__ADDON_ID__   = xbmcaddon.Addon().getAddonInfo("id")
__ADDON__   = xbmcaddon.Addon(__ADDON_ID__)
__TRAKT_API__ = 'http://api-v2launch.trakt.tv'
__TRAKT_CLIENT__ = base64.urlsafe_b64decode('YjQ4NWY0Y2M5MmY2OWEzNTc0ZjI4NTI0NTE4ZDllMjk1YmNiYjE1ZGYxODlhYjhiNTAyMzI4OGQ5ZjFhYzdmNg==')
__TRAKT_SECRET__ = base64.urlsafe_b64decode('MmU5ZmQ4NzQ4MTQ1YzgzOTJmNWU4ZWU3OWE3OTBhZmEyZWUwOWFjNGRhOGQxOTgzYzNkZjBiMDdjYWZlMzljMA==')

__TVDB_APIKEY__ = base64.urlsafe_b64decode('MUI0QThDRDFCMTQwNEY0Qg==')

__HEADERS_TRAKT__ = {'Content-Type': 'application/json', 'trakt-api-key': __TRAKT_CLIENT__, 'trakt-api-version': '2'}
__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
#'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',

def abrir_url(url, post=None, header=None, code=False, erro=False):

    if header == None:
        header = __HEADERS__

    #print header
    if post:
        req = urllib2.Request(url, data=post, headers=header)
    else:
        req = urllib2.Request(url, headers=header)
    


    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as response:
        if erro == True:
            return str(response.code), "asd"

    link=response.read()


    if code:
        return str(response.code), link

    response.close()
    return link


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

                    resultado = abrir_url(__TRAKT_API__+'/oauth/token', post=json.dumps(post), header=__HEADERS_TRAKT__)
                    resultado = json.loads(resultado)

                    token = resultado['access_token']
                    refresh = resultado['refresh_token']

                    __HEADERS_TRAKT__['Authorization'] = 'Bearer %s' % token

                    resultado = abrir_url(__TRAKT_API__+'/users/me', header=__HEADERS_TRAKT__)
                    resultado = json.loads(resultado)

                    utilizador = resultado['username']

                    __ADDON__.setSetting('utilizadorTrakt', utilizador)
                    __ADDON__.setSetting('tokenTrakt', token)
                    __ADDON__.setSetting('refreshTrakt', refresh)
                else:
                    raise Exception()
    except:
        __ADDON__.openSettings()

def loggedIn():
    if not (__ADDON__.getSetting('utilizadorTrakt') == '' or __ADDON__.getSetting('tokenTrakt') == '' or __ADDON__.getSetting('refreshTrakt') == ''):
        return True
    else:
        return False

def getTrakt(url, post=None, login=True):
    try:
        if not post == None:
            post = json.dumps(post)

        if __ADDON__.getSetting('utilizadorTrakt') == '' or __ADDON__.getSetting('tokenTrakt') == '' or __ADDON__.getSetting('refreshTrakt') == '':
            return abrir_url(url, post=post, header=__HEADERS_TRAKT__)


        __HEADERS_TRAKT__['Authorization'] = 'Bearer %s' % __ADDON__.getSetting('tokenTrakt')



        link = __TRAKT_API__+url

        codigo, conteudo = abrir_url(url, post=post, header=__HEADERS_TRAKT__, code=True, erro=True)

        if codigo != '405' and codigo != '401':
            return conteudo

        tokenPost = {'client_id': __TRAKT_CLIENT__, 'client_secret': __TRAKT_SECRET__, 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'refresh_token', 'refresh_token': __ADDON__.getSetting('refreshTrakt')}
        #print "~~~~~~~~~~~~~~~~~ Trakt MrPiracy"
        #pprint.pprint(tokenPost)

        __HEADERS_TRAKT_v2__ = {'Content-Type': 'application/json', 'trakt-api-key': __TRAKT_CLIENT__, 'trakt-api-version': '2'}

        resultado = abrir_url(__TRAKT_API__+'/oauth/token', post=json.dumps(tokenPost), header=__HEADERS_TRAKT_v2__)
        resultado = json.loads(resultado)


        #pprint.pprint(resultado)

        token = resultado['access_token']
        refresh = resultado['refresh_token']

        __ADDON__.setSetting('tokenTrakt', token)
        __ADDON__.setSetting('refreshTrakt', refresh)

        __HEADERS_TRAKT__['Authorization'] = 'Bearer %s' % token

        resultado = abrir_url(link, post=post, header=__HEADERS_TRAKT__)

        return resultado

    except:
        pass

def getFilme(idIMDB, categoria):
    url = 'http://api-v2launch.trakt.tv/movies/%s?extended=full,images' % idIMDB
    urlpt = 'http://api-v2launch.trakt.tv/movies/%s/translations/pt' % idIMDB

    resultado = abrir_url(url, header=__HEADERS_TRAKT__)
    resultado = json.loads(resultado)

    resultadopt = abrir_url(urlpt, header=__HEADERS_TRAKT__)
    resultadopt = json.loads(resultadopt)

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
        resultado2 = abrir_url(url2, header=__HEADERS__)
        resultado2 = json.loads(resultado2)

        poster = resultado2["Poster"]
    else:
        poster = resultado["images"]["poster"]["full"]

    if resultado["images"]["fanart"]["full"] is None:
        url2 = 'http://www.omdbapi.com/?i=%s&plot=full&r=json' % idIMDB
        resultado2 = abrir_url(url2, header=__HEADERS__)
        resultado2 = json.loads(resultado2)

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

    resultado = abrir_url(url, header=__HEADERS_TRAKT__)
    resultado = json.loads(resultado)

    if idIMDB == 'tt3830558':
        tvdbSerie = '300280'
    else:
        tvdbSerie = resultado["ids"]["tvdb"]

    urlTVDB = 'http://thetvdb.com/api/%s/series/%s/all/pt.zip' % (__TVDB_APIKEY__, tvdbSerie)

    resultadopt = abrir_url(urlTVDB)

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

    resultado = abrir_url(url, header=__HEADERS_TRAKT__)
    resultado = json.loads(resultado)

    if idIMDB == 'tt3830558':
        idTVDB = '300280'
    else:
        idTVDB = resultado["ids"]["tvdb"]

    serieNome = resultado['title']
    traktid = resultado["ids"]["trakt"]
    data = {}
    url = 'http://thetvdb.com/api/%s/series/%s/default/%s/%s/pt.xml' % (__TVDB_APIKEY__, idTVDB, temporada, episodio)

    soup = BeautifulSoup(abrir_url(url, header=__HEADERS__))


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
    return getTrakt(__TRAKT_API__+'/sync/history', post={"movies": [{"ids": {"imdb": imdb}}]}, login=True)


def marknotwatchedFilmeTrakt(imdb):
    if not imdb.startswith('tt'): imdb = 'tt' + imdb
    return getTrakt(__TRAKT_API__+'/sync/history/remove', post={"movies": [{"ids": {"imdb": imdb}}]}, login=True)

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
    return link

