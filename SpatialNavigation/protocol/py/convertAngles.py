def toMath(angle):
	
	if -90 < angle < 90:
		angle =  90 - angle
	elif 90 <= angle <= 180:
		angle =  90 + (360 - angle)
	elif -180 <= angle <= -90:		
		angle =  270 - (180 + angle)
	
	return angle
	
def toVizard(angle):

	if 0 <= angle < 270:
		angle = 90 - angle
	elif 270 <= angle <= 360:
		angle =  90 + (360 - angle)
	
	return angle