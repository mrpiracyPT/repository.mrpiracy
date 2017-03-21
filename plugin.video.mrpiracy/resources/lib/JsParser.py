#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class JsParser(object):
    def __init__(self):
        self.Var = []
        
    
    def GetBeetweenParenth(self,str):
        #Search the first (
        s = str.find('(')
        if s == -1:
            return ''
            
        n = 1
        e = s + 1
        while (n > 0) and (e < len(str)):
            c = str[e]
            if c == '(':
                n = n + 1
            if c == ')':
                n = n - 1
            e = e + 1
            
        s = s + 1
        e = e - 1
        return str[s:e]

    def SafeEval(self,str):
        f = re.search('[^0-9+-.\(\)]',str)
        if f:
            #xbmc.log('Wrong parameter to Eval : ' + str)
            return 0
        return eval(str)
        
    def evalJS(self,JScode,tmp):
        #https://nemisj.com/python-api-javascript/
        
        JScode = JScode.replace(' ','')
        
        #Simple replacement
        JScode = JScode.replace('String.fromCharCode', 'chr')
        JScode = JScode.replace('.charCodeAt(0)', '')
        JScode = JScode.replace('tmp.length', str(len(tmp)))
        
        #xbmc.log('avant ' + JScode)
            
        #Eval Number
        modif = True
        while (modif):
            modif = False
            #Remplacement en virant parenthses
            r = re.search('[^a-z](\([0-9+-]+\))',JScode)
            if r:
                JScode = JScode.replace(r.group(1),str(self.SafeEval(r.group(1))))
                modif = True
            #remplacement en laissant parenthses
            r = re.search('[\(\),]([0-9+-]+[+-][0-9]+)[\(\),]',JScode)
            if r:
                JScode = JScode.replace(r.group(1),str(self.SafeEval(r.group(1))))
                modif = True
            #slice
            r = re.search('tmp\.slice\((-*[0-9]+)(?:,(-*[0-9]+))*\)',JScode)
            if r:
                if r.group(2):
                    JScode = JScode.replace(r.group(0), str(ord(tmp[int(r.group(1)):int(r.group(2))][0])) )
                else:
                    JScode = JScode.replace(r.group(0),str(ord(tmp[int(r.group(1)):][0])) )
                modif = True
         

        #Eval string
        modif = True
        while (modif):
            modif = False
            #Substring
            r = re.search('tmp\.substring\((-*[0-9]+)(?:,(-*[0-9]+))*\)',JScode)
            if r:
                if r.group(2):
                    JScode = JScode.replace(r.group(0),tmp[ int(r.group(1)) : int(r.group(2)) ] )
                else:
                    JScode = JScode.replace(r.group(0),tmp[ int(r.group(1)) :] )
                modif = True
            #chr
            r = re.search('chr\(([0-9]+)\)',JScode)
            if r:
                JScode = JScode.replace(r.group(0),chr(int(r.group(1))) )
                modif = True
            #join
            r = re.search('tmp\.join\((.+)\)',JScode)
            if r:
                JScode = JScode.replace(r.group(0),r.group(1).join(tmp) )
                modif = True            
        
        #On colle le tout
        JScode = JScode.replace ('+','')
        
        #xbmc.log('apres ' + JScode)
        
        return JScode
            
    def UpdateVar(self,var,value):
        for j in self.Var:
            if j[0] == var:
                self.Var[self.Var.index(j)] = (var,value)
                return
        self.Var.append((var,value))
            
    def ReplaceVar(self,JScode):
        modif = True
        while (modif):
            modif = False
            for j in self.Var:
                if j[0] in JScode:
                    JScode = JScode.replace(j[0],'(' + j[1]+ ')')
                    modif = True
                    
        return JScode

    def ProcessJS(self,JScode,tmp):
        #Need to use in future ast.literal_eval(), need python 3
        
        #Get variable and function fixed
        function = re.compile('function ([\w_]+\(\)) *{\s*return ([^;]+)').findall(JScode)
        if function:
            for i,j in function:
                self.UpdateVar(i,j)
 
        #xbmc.log(str(self.Var))
  
        #Extract principal chain
        f = re.search('var str = (.+?);',JScode)
        if not f:
            return ''
        JScode = f.group(1)
        
        #Update code with replace fixed fonctions
        JScode = self.ReplaceVar(JScode)
        
        #eval code
        JScode = self.evalJS(JScode,tmp)
        
        return JScode