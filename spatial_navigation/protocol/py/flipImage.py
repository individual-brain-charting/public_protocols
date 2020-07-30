import viz

def flipImage(axis):
	
	#Flip rendered image horizontally
	
	if axis != False:
		flipWindow = viz.addWindow(size=(1,1),pos=(0,1),clearMask=0,order=100)
		flipWindow.setView(viz.addView(scene=viz.addScene()))
		import vizfx.postprocess.manager as pp
		from vizfx.postprocess.transform import FlipEffect
		pp.getEffectManager(flipWindow).setRenderBufferMode(pp.READ_FRAME_BUFFER)
		
		if axis == 'horizontal':
			pp.addEffect(FlipEffect(horizontal=True),window=flipWindow)
		elif axis == 'vertical':
			pp.addEffect(FlipEffect(vertical=True),window=flipWindow)
	else:
		pass