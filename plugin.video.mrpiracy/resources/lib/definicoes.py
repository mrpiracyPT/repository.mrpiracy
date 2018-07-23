#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs,sys,urllib,urllib2,unicodedata,re,urlparse,json,base64
import threading
from datetime import datetime
import ast

import controlo

def getQualidade():
	return controlo.addon.getSetting('qualidadeFilmes')

def getCookie():
	return 'username='+controlo.addon.getSetting('tokenMrpiracy')

def bruteforceconvert(str):
	controlo.log("dicionario")
	dicionario = {
	u"\\xe1" : u"á", "\xe1": u"á",
	u"\\xe9" : u"é", "\xe9" : u"é",
	u"\\xe7" : u"ç", "\xe7" : u"ç",
	u"\\xe3" : u"ã", "\xe3" : u"ã",
	u"\\xf3" : u"ó", "\xf3" : u"ó",
	u"\\xed" : u"í", "\xed" : u"í", 
	u"\\xea" : u"ê", "\xea" : u"é"}

	for k, v in dicionario.iteritems():
		controlo.log(unicode(k, errors='ignore')+" "+v)
		str.replace(k, v)
	return str.replace("\\xe1", "!", "\xe1")

def getListCategoria():
	cat = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'categorias.mrpiracy')).replace('"', "'")
	return cat

def getCategoria(id):
	#cat = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'categorias.mrpiracy')).replace(": u", ": ").replace("'", '"').replace("{u", "{").replace(", u", ", ").replace('"', "'")
	#cats = re.compile("'categorias':\s*u?'(.*?)',\s*u?'id_categoria':\s*u?'(.+?)'").findall(cat)
	cat = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'categorias.mrpiracy')).replace('"', "'")
	for c in ast.literal_eval(cat):
		if int(id) == 0:
			return ''
		if int(c['id_categoria']) == int(id):
			try:
				cat = c['categorias'].decode('utf-8')
			except:
				cat = c['categorias'].encode('utf-8')
			return cat
	
	"""if int(id) == 0:
		return ''
	
	for c, i in cats:
		if int(i) == int(id):
			return c"""

	return ''

def vista_menu():
	opcao = controlo.addon.getSetting('menuView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51")

def vista_filmesSeries():
	opcao = controlo.addon.getSetting('filmesSeriesView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
	elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
	elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
	elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
	elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
	elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")

def vista_temporadas():
	opcao = controlo.addon.getSetting('temporadasView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")

def vista_episodios():
	opcao = controlo.addon.getSetting('episodiosView')
	if opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
	elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
	elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")