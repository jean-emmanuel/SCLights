#!/usr/bin/env python
# encoding: utf-8
"""
Sebkha-Chott Lights Simulator
Simule les 4 barres led + découpes contrôlées par qlc+
"""

port = 7770

import wx
import liblo as osc

class SCLights(wx.Frame):
    def __init__(self, parent=None, title='SC Lights Simulator', pos=(100,100), size=(260,520)):
        wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size)
        self.panel = wx.Panel(self, id=-1,pos=(0,0),size=size)
        self.panel.SetBackgroundColour([30,30,30])
        
        
        self.colors = {'Red':0,'Green':1,'Blue':2,'White':3}
        self.barres = {}
        self.decoupes = {}
        self.labels = {}
        
        self.barres['CJ'] = [wx.Panel(self.panel, id=-1, pos=(20,40), size=(41,401)),[],[],[],[]]
        self.barres['BJ'] = [wx.Panel(self.panel, id=-1, pos=(80,40), size=(41,401)),[],[],[],[]]
        self.barres['BC'] = [wx.Panel(self.panel, id=-1, pos=(140,40), size=(41,401)),[],[],[],[]]
        self.barres['CC'] = [wx.Panel(self.panel, id=-1, pos=(200,40), size=(41,401)),[],[],[],[]]
        
        self.labels['CJ'] = wx.StaticText(self.panel, id=-1, label='CJ', pos=(30,20), size=(40,20))
        self.labels['BJ'] = wx.StaticText(self.panel, id=-1, label='BJ', pos=(90,20), size=(40,20))
        self.labels['BC'] = wx.StaticText(self.panel, id=-1, label='BC', pos=(150,20), size=(40,20))
        self.labels['CC'] = wx.StaticText(self.panel, id=-1, label='CC', pos=(210,20), size=(40,20))
        
        
        self.decoupes['Jardin'] = wx.Panel(self.panel, id=-1, pos=(20,480), size=(40,20))
        self.decoupes['Cour'] = wx.Panel(self.panel, id=-1, pos=(80,480), size=(40,20))
        self.decoupes['Tyran'] = wx.Panel(self.panel, id=-1, pos=(140,480), size=(40,20))
        self.decoupes['Jeannot'] = wx.Panel(self.panel, id=-1, pos=(200,480), size=(40,20))
        
        self.labels['Jardin'] = wx.StaticText(self.panel, id=-1, label='Jardin', pos=(20,460), size=(40,20))
        self.labels['Cour'] = wx.StaticText(self.panel, id=-1, label='Cour', pos=(80,460), size=(40,20))
        self.labels['Tyran'] = wx.StaticText(self.panel, id=-1, label='Tyran', pos=(140,460), size=(40,20))
        self.labels['Jeannot'] = wx.StaticText(self.panel, id=-1, label='Jeannot', pos=(200,460), size=(40,20))


        for i in self.barres.keys():
            self.barres[i][0].SetBackgroundColour([50,50,50])
            
            for n in range(8):
                self.barres[i][1].append(wx.Panel(self.barres[i][0], id=-1, pos=(1,1+n*50), size=(9,49)))
                self.barres[i][1][n].SetBackgroundColour([0,0,0])
                self.barres[i][2].append(wx.Panel(self.barres[i][0], id=-1, pos=(11,1+n*50), size=(9,49)))
                self.barres[i][2][n].SetBackgroundColour([0,0,0])
                self.barres[i][3].append(wx.Panel(self.barres[i][0], id=-1, pos=(21,1+n*50), size=(9,49)))
                self.barres[i][3][n].SetBackgroundColour([0,0,0])
                self.barres[i][4].append(wx.Panel(self.barres[i][0], id=-1, pos=(31,1+n*50), size=(9,49)))
                self.barres[i][4][n].SetBackgroundColour([0,0,0])
        
        for i in self.decoupes.keys():
            self.decoupes[i].SetBackgroundColour([0,0,0])
        
        for i in self.labels.keys():
            self.labels[i].SetForegroundColour('#fff')
            
    def start_osc(self):
        self.server = osc.ServerThread(port)
        self.server.register_methods(self)
        self.server.start()

    @osc.make_method(None, 'i')
    def update(self,path,args):
        wx.CallAfter(self.deferUpdate,path,args)
    
    def deferUpdate(self,path,args):
        path = path.split('/')
        val = max(0,min(255,args[0]))
        
        if 'Segment' in path: 

            raw_segment = path[4]
            if raw_segment == 'All':
                segments = range(8)
            elif int(raw_segment) in [1,2,3,4,5,6,7,8]:
                segments = [abs(int(raw_segment)-8)]
                

            for i in segments:
            
                if path[2] != 'White':
                    color = [0,0,0]
                    color[self.colors[path[2]]] = val

                    wx.CallAfter(self.deferSetBG,self.barres[path[1]][self.colors[path[2]]+1][i],color)
                else:
                    color = [val,val,val]
                    wx.CallAfter(self.deferSetBG,self.barres[path[1]][self.colors[path[2]]+1][i],color)
        
        if 'Decoupes' in path:
            wx.CallAfter(self.deferSetBG,self.decoupes[path[2]],[val,val,val])
            
        if 'AllStop' in path:
            for i in self.barres.keys():            
                for n in range(8):
                    self.barres[i][1][n].SetBackgroundColour([0,0,0])
                    self.barres[i][2][n].SetBackgroundColour([0,0,0])
                    self.barres[i][3][n].SetBackgroundColour([0,0,0])
                    self.barres[i][4][n].SetBackgroundColour([0,0,0])
            for i in self.decoupes.keys():
                self.decoupes[i].SetBackgroundColour([0,0,0])
                
    def deferSetBG(self,panel,color):
        panel.SetBackgroundColour(color)



app = wx.App()
mainFrame = SCLights()
mainFrame.Show()
mainFrame.start_osc()
app.MainLoop()
