import datetime
import viz

# UNIQUE names!!!

class myTimer():

	def __init__(self,dateFormat = '%d.%m.%Y', timeFormat = '%H%M%S'):
		
		self.dateFormat = dateFormat
		self.timeFormat = timeFormat
		self.started = False
	
	# timer methods to calculate time differences
	def start(self):
		
		self.startTick = viz.tick()
		self.started = True
		
	def delta(self):
		
		if self.started == False:
			self.curDelta = '0:00:00.000'
		elif self.started == True:	
			self.curDelta = datetime.timedelta(0,viz.tick()-self.startTick)
			
			if self.timeFormat == '%S':
				self.curDelta = "{:.6f}".format(self.curDelta.total_seconds())
			else:	
				self.curDelta = str(self.curDelta)[:-3]
		
		return self.curDelta
	
	# timer methods to get current date or time
	def date(self):
		
		self.curDateTime = datetime.datetime.now()
		self.curDate = self.curDateTime.strftime(self.dateFormat)
		return self.curDate
		
	def time(self):
		
		self.curDateTime = datetime.datetime.now()
		self.curTime = self.curDateTime.strftime(self.timeFormat)
		if '%f' in self.timeFormat:
			self.curTime = self.curTime[:-3]
		return self.curTime

	def getState(self):
		
		return self.started