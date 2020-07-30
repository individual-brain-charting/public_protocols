# -*- coding: utf-8 -*-

import viz
import vizdlg
import vizact
import viztask


class createPanel(vizdlg.Panel):

	def __init__(self, fullscreen = False,backgroundColor = viz.GRAY,**kw):
		
		vizdlg.Panel.__init__(self,**kw)		# init Dialog class
		
		viz.link(viz.CenterCenter,self)			# link the base panel to center of screen
		
		if fullscreen == True:
			self.background.setScale(100,100,1)
	
# --------------------
# show & hide messages
# --------------------
	
	def redraw(self):
		self.dirtyLayout(recurse = True)
	
	def positionPanel(self,position):
		
		viz.link(viz.CenterCenter,self.panel,offset = position)	# text offset in pixels (x,y,z)
	
	def hide(self, fade = 0):
		
		# let panel fade out
		self.addAction(vizact.fadeTo(0,time=fade))
		
		# let elements of panel fade out
		for item in self.getItems():
			if type(item) is (vizdlg.Panel):
				for subItem in item.getItems():
					subItem.addAction(vizact.fadeTo(0,time=fade))
			else:
				item.addAction(vizact.fadeTo(0,time=fade))
	
	def show(self, fade = 0):
		
		# let panel fade out
		self.addAction(vizact.fadeTo(1,time=fade))
		
		# let elements of panel fade out
		for item in self.getItems():
			if type(item) is (vizdlg.Panel):
				for subItem in item.getItems():
					subItem.addAction(vizact.fadeTo(1,time=fade))
			else:
				item.addAction(vizact.fadeTo(1,time=fade))