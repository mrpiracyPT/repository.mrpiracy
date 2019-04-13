#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, base64
import xbmcgui
import xbmc
import xbmcvfs
import time
import urllib
import urllib2
import re
import sys
import traceback
import json
import Trakt
import Database
from t0mm0.common.net import Net
import mrpiracy
import definicoes
import controlo
import ast

__HEADERS__ = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}


#enen92 class (RatoTv) adapted for MrPiracy.xyz addon

class Player(xbmc.Player):
    def __init__(self, url, idFilme, pastaData, temporada, episodio, nome, logo, imdb):
        xbmc.Player.__init__(self)
        self.url=url

        self.temporada=temporada
        self.episodio=episodio
        self.playing = True
        self.tempo = 0
        self.tempoTotal = 0
        self.idFilme = idFilme
        self.pastaData = xbmc.translatePath(pastaData)
        self.nome = nome
        self.logo = logo
        self.imdb = imdb
        self.API_SITE = controlo.API_SITE

        if not xbmcvfs.exists(os.path.join(pastaData,'tracker')):
            xbmcvfs.mkdirs(os.path.join(pastaData,'tracker'))


        if self.temporada != 0 and self.episodio != 0:
            self.pastaVideo = os.path.join(self.pastaData,'tracker',str(self.idFilme)+'_S'+str(self.temporada)+'x'+str(self.episodio)+'.mrpiracy')
            self.content = 'episode'
        else:
            self.pastaVideo = os.path.join(self.pastaData,'tracker',str(self.idFilme)+'.mrpiracy')
            self.content = 'movie'



    def onPlayBackStarted(self):
        #print '=======> player Start'
        self.tempoTotal = self.getTotalTime()
        #print '==========> total time'+str(self.tempoTotal)
        if self.content == 'episode':
            Trakt.checkInEpisodioTrakt(self.imdb, self.temporada, self.episodio)
        elif self.content == 'movie':
            Trakt.checkInFilmeTrakt(self.imdb)
        if xbmcvfs.exists(self.pastaVideo):
            #print "Ja existe um ficheiro do filme"

            f = open(self.pastaVideo, "r")
            tempo = f.read()
            tempoAux = ''
            minutos,segundos = divmod(float(tempo), 60)
            if minutos > 60:
                horas,minutos = divmod(minutos, 60)
                tempoAux = "%02d:%02d:%02d" % (horas, minutos, segundos)
            else:
                tempoAux = "%02d:%02d" % (minutos, segundos)

            dialog = xbmcgui.Dialog().yesno('MrPiracy', u'Já começaste a ver antes.', 'Continuas a partir de %s?' % (tempoAux), '', 'Não', 'Sim')
            if dialog:
                self.seekTime(float(tempo))



    def onPlayBackStopped(self):
        #print 'player Stop'
        self.playing = False
        
        #print 'self.time/self.totalTime='+str(self.tempo/self.tempoTotal)
        if (self.tempo/self.tempoTotal > 0.90):

            #self.adicionarVistoBiblioteca()
            self.adicionarVistoSite()

            try:
                xbmcvfs.delete(self.pastaVideo)
                xbmcvfs.delete(self.pastaVideoTotal)
            except:
                print "Não apagou"
                pass
        else:
            Trakt.checkOutTrakt()


    def adicionarVistoSite(self):
        links = self.url.split('/')
        opcao = controlo.addon.getSetting('marcarVisto')
        colocar = 0
        resultado = controlo.abrir_url(self.url, header=controlo.headers, cookie=definicoes.getCookie())
        resultado = json.loads(resultado)[0]

        if self.content == 'episode':
            WasAlreadySeen = mrpiracy.mrpiracy().getVistoEpisodio(self.idFilme)
        elif self.content == 'movie':
            WasAlreadySeen = mrpiracy.mrpiracy().getVistoFilme(self.idFilme)

        if 'filme' in self.url:
            id_video = resultado['id_video']
            imdb = resultado['IMBD']
            post = {'id_filme': id_video}
            url = self.API_SITE+'index.php?action=marcar-visto-filme&idFilme='+id_video
            tipo = 0
        elif 'serie' in self.url:
            imdb = resultado['fotoSerie'].split('/')[-1].split('.')[0]
            id_video = resultado['id_serie']
            temporadas = resultado['temporada']
            episodios = resultado['episodio']
            post = {'id_serie': id_video, 'temporada': temporadas, 'episodio':episodios}
            url = (self.API_SITE+'index.php?action=marcar-visto-episodio&idSerie=%s&temporada=%s&episodio=%s' % (id_video, temporadas, episodios) )
            tipo = 1
        elif 'anime' in self.url:
            imdb = resultado['fotoSerie'].split('/')[-1].split('.')[0]
            id_video = resultado['id_serie']
            temporadas = resultado['temporada']
            episodios = resultado['episodio']
            post = {'id_anime': id_video, 'temporada': temporadas, 'episodio':episodios}
            url = (self.API_SITE+'index.php?action=marcar-visto-episodio&idSerie=%s&temporada=%s&episodio=%s' % (id_video, temporadas, episodios) )
            tipo = 2
            
        if opcao == '0' or opcao == '2': 
            pastaVisto=os.path.join(self.pastaData,'vistos')
            try:
                os.makedirs(pastaVisto)
            except:
                pass

            if tipo == 1 or tipo == 2:
                ficheiro = os.path.join(pastaVisto, str(id_video)+'_S'+str(temporadas)+'x'+str(episodios)+'.mrpiracy')
            elif tipo == 0:
                ficheiro = os.path.join(pastaVisto, str(id_video)+'.mrpiracy')


            if not os.path.exists(ficheiro):
                f = open(ficheiro, 'w')
                f.write('')
                f.close()
            colocar = 1

        if opcao == '1' or opcao == '2': 
            if not WasAlreadySeen:
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
        if Trakt.loggedIn():
            if 'PT' in imdb:
                imdb = re.compile('(.+?)PT').findall(imdb)[0]
            if 'pt' in imdb:
                imdb = re.compile('(.+?)pt').findall(imdb)[0]
            if tipo == 2 or tipo == 1:
                if '/' in episodios:
                    ep = episodio.split('/')
                    Trakt.markwatchedEpisodioTrakt(imdb, temporadas, ep[0])
                    Trakt.markwatchedEpisodioTrakt(imdb, temporadas, ep[1])
                elif 'e' in episodios:
                    ep = episodio.split('e')
                    Trakt.markwatchedEpisodioTrakt(imdb, temporadas, ep[0])
                    Trakt.markwatchedEpisodioTrakt(imdb, temporadas, ep[1])
                else:
                    Trakt.markwatchedEpisodioTrakt(imdb, temporadas, episodios)
            elif tipo == 0:
                Trakt.markwatchedFilmeTrakt(imdb)
            mrpiracy.mrpiracy().getTrakt()
        if colocar == 1:
            xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
            xbmc.executebuiltin("Container.Refresh")
        if colocar == 2:
            xbmc.executebuiltin("XBMC.Notification(MrPiracy,"+"Marcado como não visto"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
            xbmc.executebuiltin("Container.Refresh")
        elif colocar == 3:
            controlo.alerta('MrPiracy', 'Ocorreu um erro ao marcar como visto')

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    def adicionarVistoBiblioteca(self):
        try:
            if self.content == 'episode':
                Database.markwatchedEpisodioDB(self.idFilme, self.temporada, self.episodio)
                if Trakt.loggedIn():
                    Trakt.markwatchedEpisodioTrakt(self.idFilme, self.temporada, self.episodio)
            elif self.content == 'movie':
                Database.markwatchedFilmeDB(self.idFilme)
                if Trakt.loggedIn():
                    Trakt.markwatchedFilmeTrakt(self.idFilme)
        except:
            pass

    def adicionarVistoBiblioteca2(self):
        pastaVisto=os.path.join(self.pastaData,'vistos')

        try:
            os.makedirs(pastaVisto)
        except:
            pass

        if int(self.temporada) != 0 and int(self.episodio) != 0:
            ficheiro = os.path.join(pastaVisto, str(self.idFilme)+'_S'+str(self.temporada)+'x'+str(self.episodio)+'.mrpiracy')
        else:
            ficheiro = os.path.join(pastaVisto, str(self.idFilme)+'.mrpiracy')


        if not os.path.exists(ficheiro):
            f = open(ficheiro, 'w')
            f.write('')
            f.close()
            xbmc.executebuiltin("XBMC.Notification(MrPiracy.win,"+"Marcado como visto"+","+"6000"+","+ self.logo+")")
            xbmc.executebuiltin("Container.Refresh")
        else:
            print "Já foi colocado antes"

           


    def trackerTempo(self):
        try:
            self.tempoTotal = self.getTotalTime()
            self.tempo = self.getTime()
            f = open(self.pastaVideo, mode="w")
            f.write(str(self.tempo))
            f.close()
        except:
            #traceback.print_exc()
            print "Não gravou o conteudo em %s" % self.pastaVideo
