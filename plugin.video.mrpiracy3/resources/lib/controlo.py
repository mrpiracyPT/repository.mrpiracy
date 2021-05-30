#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs,sys,urllib,unicodedata,re,json,base64,gzip
import threading
from datetime import datetime
from random import choice

try:
    # For Python 3.0 and later
    import urllib.request
    from urllib.error import URLError as UrlError
except ImportError:
    # Fall back to Python 2's urllib2
    import urllib2
    from urllib2 import URLError as UrlError


date_format = "%m/%d/%Y"
addonInfo = xbmcaddon.Addon().getAddonInfo
addon = xbmcaddon.Addon(addonInfo("id"))
addonFolder = addon.getAddonInfo('path')
definicoes = xbmcaddon.Addon().getSetting
artFolder = os.path.join(addonFolder,'resources','img')
fanart = os.path.join(addonFolder,'fanart.jpg')
skin = 'v3'

dialog = xbmcgui.Dialog()
progressDialog = xbmcgui.DialogProgress()
progressDialogBG = xbmcgui.DialogProgressBG()
windowDialog = xbmcgui.WindowDialog()

alerta = xbmcgui.Dialog().ok
select = xbmcgui.Dialog().select
simNao = xbmcgui.Dialog().yesno
mensagemprogresso = xbmcgui.DialogProgress()
teclado = xbmc.Keyboard

setSetting = xbmcaddon.Addon().setSetting

pastaDados = xbmcvfs.translatePath(addon.getAddonInfo('profile'))

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.7', 'Content-Type': 'application/json'}
dataHoras = datetime.now()
API = base64.urlsafe_b64decode('aHR0cHM6Ly9tcmFwaS54eXov')
API_SITE = base64.urlsafe_b64decode('aHR0cHM6Ly9tcmFwaS54eXovYXBpbmV3Lw==')#aHR0cDovL21wYXBpLm1sL2FwaS8=
SITE = base64.urlsafe_b64decode('aHR0cDovL21ycGlyYWN5LmdxLw==')

condVisibility = xbmc.getCondVisibility

IE_USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
OPERA_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97'
IOS_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1'
ANDROID_USER_AGENT = 'Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
EDGE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4136.7 Safari/537.36'
SAFARI_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'

_USER_AGENTS = [FF_USER_AGENT, OPERA_USER_AGENT, EDGE_USER_AGENT, CHROME_USER_AGENT, SAFARI_USER_AGENT]
RAND_UA = choice(_USER_AGENTS)

try:
    import ssl
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
except:
    pass

controlFile = os.path.join(xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.mrpiracy3/'), '1-1-0.mrpriacy')


def installAddon(addon_id):
    addon_path = os.path.join(transPath('special://home/addons'), addon_id)
    if not os.path.exists(addon_path) == True:
        xbmc.executebuiltin('InstallAddon(%s)' % (addon_id))

def yesnoDialog(line1, line2, line3, heading=addonInfo('Name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1+ '[CR]' +line2+ '[CR]' + line3, nolabel, yeslabel)

def openSettings(query=None, id=addonInfo('id')):
    try:
        idle()
        execute('Addon.OpenSettings(%s)' % id)
        if query is None:
            raise Exception()
        c, f = query.split('.')
        if int(getKodiVersion()) >= 18:
            execute('SetFocus(%i)' % (int(c) - 100))
            execute('SetFocus(%i)' % (int(f) - 80))
        else:
            execute('SetFocus(%i)' % (int(c) + 100))
            execute('SetFocus(%i)' % (int(f) + 200))
    except Exception:
        return


def quote_plus(url):
    parsed = ''
    try:
        parsed = urllib.quote_plus(url)
    except:
        parsed = urllib.parse.quote_plus(url)

    return parsed

def urlencode(data):
    urlencode = ''
    try:
        urlencode = urllib.urlencode(data)
    except:
        urlencode = urllib.parse.urlencode(data)

    return urlencode

def addDir(name,url,modo,iconimage,pagina=False,tipo=False,infoLabels=False,poster=False,visto=False, menuO=False,favorito=False, agendado=False, aseguir=False):
    menu = []
    if infoLabels: infoLabelsAux = infoLabels
    else: infoLabelsAux = {'Title': name}

    if poster: posterAux = poster
    else: posterAux = iconimage

    u=sys.argv[0]+"?url="+quote_plus(url)+"&modo="+modo
    ok=True
    fan = fanart
    overlay = 6
    playcount = 0
    if menuO:
        if favorito:
            menu.append(('Remover dos Favoritos', 'RunPlugin(%s?modo=remover-favoritos&url=%s)' % (sys.argv[0], quote_plus(url))))
        else:
            menu.append(('Adicionar aos Favoritos', 'RunPlugin(%s?modo=adicionar-favoritos&url=%s)' % (sys.argv[0], quote_plus(url))))
        if agendado:
            menu.append(('Remover dos Agendados (ver mais tarde)', 'RunPlugin(%s?modo=remover-agendar&url=%s)' % (sys.argv[0], quote_plus(url))))    
        else:
            menu.append(('Agendar (ver mais tarde)', 'RunPlugin(%s?modo=adicionar-agendar&url=%s)' % (sys.argv[0], quote_plus(url))))
        if aseguir:
            menu.append(('Não receber notificação (A Seguir)', 'RunPlugin(%s?modo=remover-aseguir&url=%s)' % (sys.argv[0], quote_plus(url))))
        else:
            menu.append(('Receber notificação (A Seguir)', 'RunPlugin(%s?modo=adicionar-aseguir&url=%s)' % (sys.argv[0], quote_plus(url))))
        if visto == True:
            menu.append(('Marcar como não visto', 'RunPlugin(%s?modo=marcar-visto&url=%s)' % (sys.argv[0], quote_plus(url))))
            overlay = 7
            playcount = 1
        elif visto == False:
            menu.append(('Marcar como visto', 'RunPlugin(%s?modo=marcar-visto&url=%s)' % (sys.argv[0], quote_plus(url))))

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

    try:
        str(name).decode('utf-8')
    except:
        pass

    infoLabelsAux["overlay"] = overlay
    infoLabelsAux["playcount"] = playcount
    liz=xbmcgui.ListItem(name)
    liz.setArt({ 'icon': iconimage, 'thumb' : iconimage , 'poster': iconimage})
    liz.setProperty('fanart_image', fan)
    liz.setInfo( type="Video", infoLabels=infoLabelsAux )
    liz.addContextMenuItems(menu, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addVideo(name,url,modo,iconimage,visto,tipo,temporada,episodio,infoLabels,poster, trailer=False,serieNome=False,favorito=False,agendado=False, aseguir=False):

    menu = []

    if tipo == 'filme':
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        #visto = checkVisto(url)
        if favorito:
            menu.append(('Remover dos Favoritos', 'RunPlugin(%s?modo=remover-favoritos&url=%s)' % (sys.argv[0], quote_plus(url))))
        else:
            menu.append(('Adicionar aos Favoritos', 'RunPlugin(%s?modo=adicionar-favoritos&url=%s)' % (sys.argv[0], quote_plus(url))))
        if agendado:
            menu.append(('Remover dos Agendados (ver mais tarde)', 'RunPlugin(%s?modo=remover-agendar&url=%s)' % (sys.argv[0], quote_plus(url))))
        else:
            menu.append(('Agendar (ver mais tarde)', 'RunPlugin(%s?modo=adicionar-agendar&url=%s)' % (sys.argv[0], quote_plus(url))))
        if aseguir:
            menu.append(('Não receber notificação (A Seguir)', 'RunPlugin(%s?modo=remover-aseguir&url=%s)' % (sys.argv[0], quote_plus(url))))
        else:
            menu.append(('Receber notificação (A Seguir)', 'RunPlugin(%s?modo=adicionar-aseguir&url=%s)' % (sys.argv[0], quote_plus(url))))
        if addon.getSetting('trailer-filmes') == 'true':
            try:
                
                idYoutube = trailer.split('?v=')[-1].split('/')[-1].split('?')[0].split('&')[0]
                linkTrailer = 'plugin://plugin.video.youtube/?action=play_video&videoid='+idYoutube
                
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
        menu.append(('Marcar como não visto', 'RunPlugin(%s?modo=marcar-n-visto&url=%s)' % (sys.argv[0], quote_plus(url))))
        overlay = 7
        playcount = 1
    elif visto == False:
        menu.append(('Marcar como visto', 'RunPlugin(%s?modo=marcar-visto&url=%s)' % (sys.argv[0], quote_plus(url))))


    if not serieNome:
        serieNome = ''

    u=sys.argv[0]+"?url="+quote_plus(url)+"&modo="+modo
    ok=True
    #&name="+urllib.quote_plus(name)+"
    infoLabels["overlay"] = overlay
    infoLabels["playcount"] = playcount
    
    try:
        str(name).decode('utf-8')
    except:
        pass
    
    liz=xbmcgui.ListItem(name)
    liz.setArt({ 'icon': iconimage, 'thumb' : iconimage })
    liz.setProperty('fanart_image', poster)
    liz.setInfo( type="Video", infoLabels=infoLabels )

    if linkTrailer != '':
        menu.append(('Ver Trailer', 'PlayMedia(%s)' % (linkTrailer)))

    #menu.append(('Marcar como visto (Site)', 'RunPlugin(%s?mode=16&url=%s)' % (sys.argv[0], quote_plus(url))))

    menu.append(('Download', 'RunPlugin(%s?modo=download&url=%s)'%(sys.argv[0], quote_plus(url))))
    liz.addContextMenuItems(menu, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def to_unicode(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def abrir_url(url, post=None, header=None, code=False, erro=False, cookie=None, retrieveUrl=False):

    content = ''
    urlRidirected = ''

    if post:
        post = post.encode('utf-8')

    if header == None:
        header = headers
    else:
        
       """ for key in header:
            req.add_header(key, header[key])
            log(key+" => "+header[key])"""
    if cookie:
        header['Cookie'] = cookie

        #req.add_header('Cookie', cookie)
    if post:
        header['Content-Type'] ='application/x-www-form-urlencoded'
        #req.add_header('Content-Type', 'application/x-www-form-urlencoded')
 
    if post: 
        #req = requests.post(url, data=post, headers=header)
        req = urllib.request.Request(url, data=post, headers=header)
    else:
        req = urllib.request.Request(url,headers=header)
        #req = requests.get(url, headers=header)

    res = urllib.request.urlopen(req)
    
    content = res.read()
    if retrieveUrl:
        return content, res.url
    return content

    #if sys.version[0] == '2':

    """try:
        response = urllib2.urlopen(req,context=context)
    except:
        try:
            response = urllib2.urlopen(req)
        except UrlError as er:
            
            log(str(str(er)))
            return str(str(er)), "asd"

    try:
        content=gzip.decompress(response.read())
    except:
        pass

    log("content-encoding: "+str(response.info().get_content_charset()))

    try:
        urlRidirected = response.geturl()
    except:
        urlRidirected = response.url

    log("url: "+urlRidirected)

    response.close()

    if retrieveUrl:
        return content, urlRidirected

    if code:
        return str(response.code), content
    return content"""



    """if post:
        req = urlopen(url, data=post, headers=header)
    else:
        req = urlopen(url, headers=header)

    try:
        response = urlopen(req,context=context)
    except:
        try:
            response = urlopen(req)
        except:
            if erro == True:
                log(str("asd"))
                return str("response.code"), "asd"
    
    link=response.read()
    
    try:
        urlRidirected = response.geturl()
    except:
        urlRidirected = response.url
    
    if 'judicial blblblblbl' in link:
        return 'DNS'
    if code:
        return str(response.code), link

    response.close()
    if retrieveUrl:
        return link, urlRidirected
    return link"""
    
def log(msg, level=xbmc.LOGINFO):
    level = xbmc.LOGINFO
    #print('[MRPIRACY]: %s' % (msg))
    xbmc.log('[MRPIRACY]: %s' % (msg), level)
    try:
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        xbmc.log('[MRPIRACY]: %s' % (msg), level)
    except Exception as e:
        try:
            a=1
        except: pass 


def escrever_ficheiro(ficheiro, conteudo):
    f = open(ficheiro, mode="w", encoding='utf8')
    f.write(str(conteudo))
    f.close()
def ler_ficheiro(ficheiro):
    f = open(ficheiro, "r", encoding='utf8')
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

def clean(text):
    command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)