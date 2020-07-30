# -*- coding: utf-8 -*-

import viz
import vizdlg
import vizact
import viztask

class displayInfo(vizdlg.Dialog):

	def __init__(self,window = viz.MainWindow, mode = 'fit',fontSize = 50,textAlignment = viz.ALIGN_CENTER,border = True,background = True, padding = 5,**kw):
		
		vizdlg.Dialog.__init__(self,**kw)
		
		self.fontSize = fontSize
		self.textAlignment = textAlignment
		self.textColor = (0,0,0)
		self.borderDesired = border
		self.bgDesired = background
		self._padding = padding
		
		# define own color theme
		blackTheme = viz.getTheme()
		blackTheme.backColor = (.5,.5,.5,1)
		blackTheme.lightBackColor = (0.6,0.6,0.6,1)
		blackTheme.darkBackColor = (0.2,0.2,0.2,1)
		blackTheme.highBackColor = (0.2,0.2,0.2,1)
		blackTheme.textColor = (self.textColor)
		
		if mode == 'fullscreen':
			self.panel = vizdlg.Panel(window, theme = blackTheme,align = vizdlg.ALIGN_CENTER,border = False, background = self.bgDesired) # add panel without border
			self.panel.background.setScale(5000,5000,1) # if fullscreen is passed, scale the background so it covers fullscreen
		elif mode == 'fit':
			self.panel = vizdlg.Panel(window, theme = blackTheme,align = vizdlg.ALIGN_CENTER, border = self.borderDesired, background = self.bgDesired, padding = self._padding) # add panel
			
		self.panel.background.alpha(1) 			# set background alpha
		viz.link(viz.CenterCenter,self.panel)	# link the panel to center of screen
	
		# switch variables to determine state of message panel
		self.textDisplayed = False
		
		# let the panel fade out to 0 at initialization (necessary for smooth fading at first usage)
		self.panel.background.addAction(vizact.fadeTo(0))	

# ------------------
# color related
# ------------------

	def setBgColor(self,color):
	
		self.panel.background.color(color)
		
	def setTextColor(self,color):
		
		self.textColor = color

# --------------------
# show & hide messages
# --------------------

	def message(self,text,fade = 0):
		
		# remove any leftover text before displaying new one
		if self.textDisplayed == True:
			self.removeText()
		
		# init text
		self.text = self.panel.addItem(viz.addText(text))	# if message should be displayed, add text item
		
		# set attributes
		self.text.fontSize(self.fontSize)
		self.text.alignment(self.textAlignment)
		self.text.color(self.textColor)
		
		# let the panel fade in
		self.panel.background.addAction(vizact.fadeTo(1,time=fade))
		
		# fade in of the text (if desired)
		self.text.addAction(vizact.fadeTo(1,time=fade))
	
		self.textDisplayed = True		# switch the state to text being displayed
	
	def removeText(self):
		
		if self.textDisplayed == True:
		
			self.panel.removeItem(self.text)
			self.textDisplayed = False
			
		elif self.textDisplayed == False:
			print('Display Info module: No text to be hidden, ignoring text hide command.')

	def removeItems(self,fadeTime = 0):
		
		for item in self.panel.getItems():
			itemType = type(item)
			# only if it is not a text item, remove item
			if itemType.__doc__ != 'VizText object':
				self.panel.removeItem(item)

	def positionPanel(self,position):
		
		viz.link(viz.CenterCenter,self.panel,offset = position)	# text offset in pixels (x,y,z)
	
	def setFontsize(self,fontSize):
		
		self.fontSize = fontSize
	
	def addImage(self,image, fade = 0):
		
		# let the panel fade in
		self.panel.background.addAction(vizact.fadeTo(1,time=fade))
		
		self.image = self.panel.addItem(image)
	
	def hide(self, fade = 0):
		
		# same as removeItems, but it waits for possible fading action to be completed before removing items
		def removeItemsFaded(self,fadeTime = 0):
			yield viztask.waitTime(fadeTime)
		
			for item in self.panel.getItems():
				self.panel.removeItem(item)
		
		# let panel fade out
		self.panel.background.addAction(vizact.fadeTo(0,time=fade))
		
		# let elements fade out
		for item in self.panel.getItems():
			item.addAction(vizact.fadeTo(0,time=fade))	
			viztask.schedule(removeItemsFaded(self,fadeTime = fade))
			
			self.textDisplayed = False
