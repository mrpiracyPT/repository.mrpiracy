#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs,sys,urllib,urllib2,unicodedata,re,urlparse,json,base64
import threading
from datetime import datetime



from t0mm0.common.addon import Addon

date_format = "%m/%d/%Y"
addonInfo = xbmcaddon.Addon().getAddonInfo
addon = xbmcaddon.Addon(addonInfo("id"))
addonFolder = addon.getAddonInfo('path')
definicoes = xbmcaddon.Addon().getSetting
artFolder = os.path.join(addonFolder,'resources','img')
fanart = os.path.join(addonFolder,'fanart.jpg')
skin = 'v2'
alerta = xbmcgui.Dialog().ok
select = xbmcgui.Dialog().select
simNao = xbmcgui.Dialog().yesno
mensagemprogresso = xbmcgui.DialogProgress()
teclado = xbmc.Keyboard
pastaDados = Addon(addonInfo("id")).get_profile().decode("utf-8")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.7', 'Content-Type': 'application/json'}
dataHoras = datetime.now()
API = base64.urlsafe_b64decode('aHR0cDovL21yYXBpLnh5ei8=')
API_SITE = base64.urlsafe_b64decode('aHR0cDovL21yYXBpLnh5ei9hcGluZXcv')
SITE = base64.urlsafe_b64decode('aHR0cDovL21ycGlyYWN5LmdxLw==')

try:
    import ssl
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
except:
    pass
def addDir(name,url,modo,iconimage,pagina=False,tipo=False,infoLabels=False,poster=False,visto=False, menuO=False,favorito=False, agendado=False):
    menu = []
    if infoLabels: infoLabelsAux = infoLabels
    else: infoLabelsAux = {'Title': name}

    if poster: posterAux = poster
    else: posterAux = iconimage

    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&modo="+modo
    ok=True
    fan = fanart
    overlay = 6
    playcount = 0
    if menuO:
        if favorito:
            menu.append(('Remover dos Favoritos', 'XBMC.RunPlugin(%s?modo=remover-favoritos&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        else:
            menu.append(('Adicionar aos Favoritos', 'XBMC.RunPlugin(%s?modo=adicionar-favoritos&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        if agendado:
            menu.append(('Remover dos Agendados (ver mais tarde)', 'XBMC.RunPlugin(%s?modo=remover-agendar&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))    
        else:
            menu.append(('Agendar (ver mais tarde)', 'XBMC.RunPlugin(%s?modo=adicionar-agendar&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        if visto == True:
            menu.append(('Marcar como não visto', 'XBMC.RunPlugin(%s?modo=marcar-visto&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
            overlay = 7
            playcount = 1
        elif visto == False:
            menu.append(('Marcar como visto', 'XBMC.RunPlugin(%s?modo=marcar-visto&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))

    if tipo == 'filme':
        fan = posterAux
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    elif tipo == 'serie':
        fan = posterAux
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    elif tipo == 'episodio':
        fan = posterAux
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    else:
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

    infoLabelsAux["overlay"] = overlay
    infoLabelsAux["playcount"] = playcount
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fan)
    liz.setInfo( type="Video", infoLabels=infoLabelsAux )
    liz.addContextMenuItems(menu, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addVideo(name,url,modo,iconimage,visto,tipo,temporada,episodio,infoLabels,poster, trailer=False,serieNome=False,favorito=False,agendado=False):

    menu = []

    if tipo == 'filme':
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        #visto = checkVisto(url)
        if favorito:
            menu.append(('Remover dos Favoritos', 'XBMC.RunPlugin(%s?modo=remover-favoritos&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        else:
            menu.append(('Adicionar aos Favoritos', 'XBMC.RunPlugin(%s?modo=adicionar-favoritos&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        if agendado:
            menu.append(('Remover dos Agendados (ver mais tarde)', 'XBMC.RunPlugin(%s?modo=remover-agendar&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        else:
            menu.append(('Agendar (ver mais tarde)', 'XBMC.RunPlugin(%s?modo=adicionar-agendar&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        if addon.getSetting('trailer-filmes') == 'true':
            try:
                idYoutube = trailer.split('?v=')[-1].split('/')[-1].split('?')[0].split('&')[0]
                linkTrailer = 'plugin://plugin.video.youtube/play/?video_id='+idYoutube
            except:
                linkTrailer = ''
        else:
            linkTrailer = ''
    elif tipo == 'serie':
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        visto = checkVisto(url, temporada, episodio)
        idIMDb = re.compile('imdb=(.+?)&').findall(url)[0]
        linkTrailer = ""
    elif tipo == 'episodio':
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        #visto = checkVisto(url, temporada, episodio)
        
        linkTrailer = ""

    overlay = 6
    playcount = 0

    

    if visto == True:
        menu.append(('Marcar como não visto', 'XBMC.RunPlugin(%s?modo=marcar-n-visto&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))
        overlay = 7
        playcount = 1
    elif visto == False:
        menu.append(('Marcar como visto', 'XBMC.RunPlugin(%s?modo=marcar-visto&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))


    if not serieNome:
        serieNome = ''

    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&modo="+modo
    ok=True
    #&name="+urllib.quote_plus(name)+"
    infoLabels["overlay"] = overlay
    infoLabels["playcount"] = playcount

    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty('fanart_image', poster)
    liz.setInfo( type="Video", infoLabels=infoLabels )

    if linkTrailer != '':
        menu.append(('Ver Trailer', 'XBMC.PlayMedia(%s)' % (linkTrailer)))

    #menu.append(('Marcar como visto (Site)', 'XBMC.RunPlugin(%s?mode=16&url=%s)' % (sys.argv[0], urllib.quote_plus(url))))

    menu.append(('Download', 'XBMC.RunPlugin(%s?modo=download&url=%s)'%(sys.argv[0], urllib.quote_plus(url))))
    liz.addContextMenuItems(menu, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def to_unicode(text):
	nfkd_form = unicodedata.normalize('NFKD', text)
	return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def abrir_url(url, post=None, header=None, code=False, erro=False, cookie=None):

    if header == None:
        header = headers
    if cookie:
        header['Cookie'] = cookie
    
    if post:
        header['Content-Type'] ='application/x-www-form-urlencoded'
        req = urllib2.Request(url, data=post, headers=header)
    else:
        req = urllib2.Request(url, headers=header)

    try:
        response = urllib2.urlopen(req,context=context)
    except:
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as response:
            if erro == True:
                log(str(response.code))
                return str(response.code), "asd"
    
    link=response.read()

    """if 'myapimp.tk' in url:
        xbmc.log(url)
        coiso = json.loads(link)
        if 'error' in coiso:
            if coiso['error'] == 'access_denied':
                xbmc.log("REFRESH")
                headers['Authorization'] = 'Bearer %s' % addon.getSetting('tokenMrpiracy')
                dados = {'refresh_token': addon.getSetting('refreshMrpiracy'),'grant_type': 'refresh_token', 'client_id': 'kodi', 'client_secret':'pyRmmKK3cbjouoDMLXNtt2eGkyTTAG' }
                
                resultado = abrir_url(base64.urlsafe_b64decode('aHR0cDovL215YXBpbXAudGsvYXBpLw==')+'token/refresh',post=json.dumps(dados), header=headers)

                resultado = json.loads(resultado)
                addon.setSetting('tokenMrpiracy', resultado['access_token'])
                addon.setSetting('refreshMrpiracy', resultado['refresh_token'])
                if post:
                    return abrir_url(url, post=post, header=header)
                else:
                    return abrir_url(url, header=header)
            if coiso['error'] == 'invalid_request' and coiso['error_description'] == 'The refresh token is invalid.':
                xbmc.log("LOGIN")
                dados = {'username': addon.getSetting('email'), 'password': addon.getSetting('password'),'grant_type': 'password', 'client_id': 'kodi', 'client_secret':'pyRmmKK3cbjouoDMLXNtt2eGkyTTAG' }
                resultado = abrir_url(base64.urlsafe_b64decode('aHR0cDovL215YXBpbXAudGsvYXBpLw==')+'login',post=json.dumps(dados), header=headers)
                resultado = json.loads(resultado)
                addon.setSetting('tokenMrpiracy', resultado['access_token'])
                addon.setSetting('refreshMrpiracy', resultado['refresh_token'])
                if post:
                    return abrir_url(url, post=post, header=header)
                else:
                    return abrir_url(url, header=header)

    """
    if 'judicial blblblblbl' in link:
        return 'DNS'
    if code:
        return str(response.code), link

    response.close()
    return link
    
def log(msg, level=xbmc.LOGNOTICE):
    level = xbmc.LOGNOTICE
    #print('[MRPIRACY]: %s' % (msg))

    try:
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        xbmc.log('[MRPIRACY]: %s' % (msg), level)
    except Exception as e:
        try:
            a=1
        except: pass 


def escrever_ficheiro(ficheiro, conteudo):
    f = open(ficheiro, mode="w")
    f.write(conteudo)
    f.close()
def ler_ficheiro(ficheiro):
    f = open(ficheiro, "r")
    conteudo =  f.read()
    f.close()
    return conteudo
def getCategoria(categoria):
    lista = json.loads(addon.getSetting('categorias'))
    return lista.get(categoria)
def getVistosFilmes(id):
    lista = json.loads(addon.getSetting('vistos_filmes'))
    return lista[id]
def getVistosSeries(id):
    lista = json.loads(addon.getSetting('vistos_series'))
    return lista[id]


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)