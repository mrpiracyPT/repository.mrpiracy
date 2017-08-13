#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs,sys,urllib,urllib2,unicodedata,re,urlparse,json,base64
import threading
from datetime import datetime

import controlo

def getQualidade():
	return controlo.addon.getSetting('qualidadeFilmes')

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