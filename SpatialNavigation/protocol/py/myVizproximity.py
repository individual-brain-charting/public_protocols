# Copyright (c) 2001-2013 WorldViz LLC.
# All rights reserved.

# Changed function removeSensor() so it will correctly report no active sensor after one has been removed

import viz
import math
import vizact
import vizmat
import viztask
import vizshape

# Default color for debug shapes
DEFAULT_DEBUG_COLOR = [1,0,1]

# Default color for activated debug shapes
DEFAULT_DEBUG_ACTIVE_COLOR = [0,1,0]

# Default priority for updating proximity sensors
DEFAULT_UPDATE_PRIORITY = viz.PRIORITY_LINKS + 1

# Proximity events
ENTER_PROXIMITY_EVENT = viz.getEventID('vizproximity_ENTER_PROXIMITY_EVENT')
EXIT_PROXIMITY_EVENT = viz.getEventID('vizproximity_EXIT_PROXIMITY_EVENT')

class ProximityEvent(viz.Event):
	"""Object used for proximity enter/exit events"""
	def __init__(self,sensor,target,manager):
		"""@args Sensor(), Target(), Manager()"""
		self.sensor = sensor
		self.target = target
		self.manager = manager

class Source(object):
	"""Base class for objects providing source position of proximity sensors/targets"""
	def getObject(self):
		return None

	def getMatrix(self):
		return viz.Matrix()

	def getPosition(self):
		return self.getMatrix().getPosition()

class MatrixSource(Source):
	"""Use static matrix object as source"""
	def __init__(self,matrix):
		self._matrix = matrix

	def __repr__(self):
		return "{}(matrix={})".format(self.__class__.__name__,self._matrix)

	def getObject(self):
		return self._matrix

	def getMatrix(self):
		return viz.Matrix(self._matrix)

	def getPosition(self):
		return self._matrix.getPosition()

class LinkableSource(Source):
	"""Use linkable object as source"""
	def __init__(self,linkable,flag=0):
		"""@arg linkable viz.VizLinkable()"""
		self._linkable = linkable
		self._flag = flag

	def __repr__(self):
		return "{}(linkable={}, flag={})".format(self.__class__.__name__,self._linkable,self._flag)

	def getObject(self):
		return self._linkable

	def getMatrix(self):
		return self._linkable.getMatrix(self._flag)

	def getPosition(self):
		return self._linkable.getPosition(self._flag)

class NodeSource(Source):
	"""Use node object as source"""
	def __init__(self,node, flag=viz.ABS_GLOBAL, name=''):
		"""@arg node viz.VizNode()"""
		self._node = node
		self._flag = flag
		self._name = name

	def __repr__(self):
		return "{}(node={}, flag={}, name={})".format(self.__class__.__name__,self._node,self._flag,repr(self._name))

	def getObject(self):
		return self._node

	def getMatrix(self):
		return self._node.getMatrix(self._flag,self._name)

def createSource(source):
	"""Create Source object from standard Vizard object (e.g. node, view, tracker, bone, matrix, ...)"""

	# Use null source if None
	if source is None:
		return Source()

	# Check for Source objects
	if isinstance(source,Source):
		return source

	# Check for matrix objects
	if isinstance(source,viz.Matrix):
		return MatrixSource(source)

	# Check for node objects
	if isinstance(source,viz.VizNode):
		return NodeSource(source)

	# Check for bone objects
	if isinstance(source,viz.VizBone):
		return LinkableSource(source,viz.AVATAR_WORLD)

	# Check for any other linkable object
	if viz._getLinkableType(source) >= 0:
		return LinkableSource(source)

	raise TypeError, 'source is not a valid Source type'

class Shape(object):
	"""Base class for objects providing shapes for proximity sensors"""
	def containsPoint(self,point):
		"""Returns whether the point is inside the shape"""
		raise NotImplementedError

	def createDebugNode(self,data):
		"""Create and return node object for visualizing proximity shape"""
		return None

class Sphere(Shape):
	"""Spherical shape for proximity sensors"""
	def __init__(self,radius,center=(0.0,0.0,0.0)):
		self._radius = radius
		self._center = tuple(center)

	def __repr__(self):
		return "{}(radius={}, center={})".format(self.__class__.__name__,self._radius,self._center)

	def containsPoint(self,point):
		"""Returns whether the point is inside the shape"""
		return vizmat.Distance(point,self._center) < self._radius

	def createDebugNode(self,data):
		"""Create and return node object for visualizing proximity shape"""
		s = vizshape.addSphere(radius=self._radius,slices=4,stacks=4,transform=viz.Matrix.translate(self._center))
		s.disable([viz.LIGHTING,viz.CULL_FACE])
		s.color(data.color)
		s.polyMode(viz.POLY_WIRE)
		return s

class Box(Shape):
	"""Box shape for proximity sensors"""
	def __init__(self,size,center=(0.0,0.0,0.0)):
		self._size = tuple(size)
		self._center = tuple(center)

		x = self._size[0] / 2.0
		y = self._size[1] / 2.0
		z = self._size[2] / 2.0

		self._extents = [ self._center[0] - x, self._center[0] + x
						, self._center[1] - y, self._center[1] + y
						, self._center[2] - z, self._center[2] + z ]

	def __repr__(self):
		return "{}(size={}, center={})".format(self.__class__.__name__,self._size,self._center)

	def containsPoint(self,point):
		"""Returns whether the point is inside the shape"""
		xmin,xmax,ymin,ymax,zmin,zmax = self._extents
		return xmin < point[0] < xmax and ymin < point[1] < ymax and zmin < point[2] < zmax

	def createDebugNode(self,data):
		"""Create and return node object for visualizing proximity shape"""
		s = vizshape.addBox(size=self._size,transform=viz.Matrix.translate(self._center))
		s.disable([viz.LIGHTING,viz.CULL_FACE])
		s.color(data.color)
		s.polyMode(viz.POLY_WIRE)
		return s

class CircleArea(Shape):
	"""2D circular area shape for proximity sensors"""
	def __init__(self,radius,center=(0.0,0.0)):
		self._radius = radius
		self._center = tuple(center[:2])

	def __repr__(self):
		return "{}(radius={}, center={})".format(self.__class__.__name__,self._radius,self._center)

	def containsPoint(self,point):
		"""Returns whether the point is inside the shape"""
		return vizmat.Distance((point[0],point[2]),self._center) < self._radius

	def createDebugNode(self,data):
		"""Create and return node object for visualizing proximity shape"""

		viz.startLayer(viz.LINE_LOOP)

		# Add slices
		slices = 10
		dtheta = 2.0 * math.pi / slices
		radius = self._radius
		sin = math.sin
		cos = math.cos
		x = self._center[0]
		y = self._center[1]
		for i in range(slices+1):
			if i == slices:
				theta = 0.0
			else:
				theta = i * dtheta
			viz.vertex( (sin(theta) * radius) + x , 0.0 , (cos(theta) * radius) + y )

		s = viz.endLayer()
		s.disable([viz.LIGHTING,viz.CULL_FACE])
		s.color(data.color)
		return s

class RectangleArea(Shape):
	"""2D rectangle area shape for proximity sensors"""
	def __init__(self,size,center=(0.0,0.0)):
		self._size = tuple(size[:2])
		self._center = tuple(center[:2])

		x = self._size[0] / 2.0
		z = self._size[1] / 2.0

		self._extents = [ self._center[0] - x, self._center[0] + x
						, self._center[1] - z, self._center[1] + z ]

	def __repr__(self):
		return "{}(size={}, center={})".format(self.__class__.__name__,self._size,self._center)

	def containsPoint(self,point):
		"""Returns whether the point is inside the shape"""
		xmin,xmax,zmin,zmax = self._extents
		return xmin < point[0] < xmax and zmin < point[2] < zmax

	def createDebugNode(self,data):
		"""Create and return node object for visualizing proximity shape"""
		xmin,xmax,zmin,zmax = self._extents
		viz.startLayer(viz.LINE_LOOP)
		viz.vertex((xmin,0,zmin))
		viz.vertex((xmin,0,zmax))
		viz.vertex((xmax,0,zmax))
		viz.vertex((xmax,0,zmin))
		s = viz.endLayer()
		s.disable([viz.LIGHTING,viz.CULL_FACE])
		s.color(data.color)
		return s

class PolygonArea(Shape):
	"""2D polygonal area shape for proximity sensors"""
	def __init__(self,points,offset=(0.0,0.0)):
		self._points = tuple( (float(p[0]),float(p[1])) for p in points )
		self._offset = tuple(offset[:2])

		cx = offset[0]
		cy = offset[1]
		self._verts = tuple( (x+cx,y+cy) for x,y in self._points )

	def __repr__(self):
		return "{}(points={}, offset={})".format(self.__class__.__name__,self._points,self._offset)

	def containsPoint(self,point):
		"""Returns whether the point is inside the shape"""
		return vizmat.pointInPolygon(self._verts,(point[0],point[2]))

	def createDebugNode(self,data):
		"""Create and return node object for visualizing proximity shape"""
		viz.startLayer(viz.LINE_LOOP)
		for x,y in self._verts:
			viz.vertex((x,0,y))
		s = viz.endLayer()
		s.disable([viz.LIGHTING,viz.CULL_FACE])
		s.color(data.color)
		return s

class PathArea(PolygonArea):
	"""2D path area specified through series of points and a radius distance from path"""
	def __init__(self,points,radius,offset=(0.0,0.0)):
		self._radius = float(radius)
		self._path = tuple( (p[0],p[1]) for p in points )

		leftSide = []
		rightSide = []
		numPoints = len(self._path)

		def vector(p):
			return (p[0],0.0,p[1])

		leftMat = viz.Matrix.translate(-radius,0,0)
		rightMat = viz.Matrix.translate(radius,0,0)

		for x in range(numPoints-1):

			begin = vector(self._path[x])
			end = vector(self._path[x+1])

			# Add begin vertices
			if x == 0:
				mat = viz.Matrix.lookat(begin,end,[0,1,0])
				mat.preTrans((0,0,-radius))
				leftSide.append( (leftMat * mat).getPosition() )
				rightSide.append( (rightMat * mat).getPosition() )

			# And joint vertices
			elif x > 0:

				prev = vector(self._path[x-1])
				curr = vector(self._path[x])
				next = vector(self._path[x+1])

				# Get incoming/outgoing rotation matrix
				inMat = viz.Matrix.lookat(prev,curr,[0,1,0])
				outMat = viz.Matrix.lookat(curr,next,[0,1,0])

				# Get angle at joint
				angle = (inMat.inverse() * outMat).getEuler()[0]

				if angle > 0.0:

					# Going to the right

					# Add intersection point to right side
					lineInMat = viz.Matrix(inMat)
					lineInMat.preTrans((radius,0,0))
					lineIn = viz.Line(begin=lineInMat.getPosition(),dir=lineInMat.getForward())
					lineOutMat = viz.Matrix(outMat)
					lineOutMat.preTrans((radius,0,0))
					lineOut = viz.Line(begin=lineOutMat.getPosition(),dir=lineOutMat.getForward())
					rightSide.append( lineIn.intersectLine(lineOut) )

					# Add extra vertices to left side
					inMat.setPosition(curr)
					leftSide.append( (leftMat * inMat).getPosition() )
					inMat.preEuler((angle * 0.5,0.0,0.0))
					leftSide.append( (leftMat * inMat).getPosition() )
					leftSide.append( (leftMat * outMat).getPosition() )

				elif angle < 0.0:

					# Going to the left

					# Add intersection point to left side
					lineInMat = viz.Matrix(inMat)
					lineInMat.preTrans((-radius,0,0))
					lineIn = viz.Line(begin=lineInMat.getPosition(),dir=lineInMat.getForward())
					lineOutMat = viz.Matrix(outMat)
					lineOutMat.preTrans((-radius,0,0))
					lineOut = viz.Line(begin=lineOutMat.getPosition(),dir=lineOutMat.getForward())
					leftSide.append( lineIn.intersectLine(lineOut) )

					# Add extra vertices to right side
					inMat.setPosition(curr)
					rightSide.append( (rightMat * inMat).getPosition() )
					inMat.preEuler((angle * 0.5,0.0,0.0))
					rightSide.append( (rightMat * inMat).getPosition() )
					rightSide.append( (rightMat * outMat).getPosition() )

				else:

					# No angle difference, skip vertices
					pass

			# Add end vertices
			if (x+1) == (numPoints-1):
				mat = viz.Matrix.lookat(begin,end,[0,1,0])
				mat.setPosition(end)
				mat.preTrans((0,0,radius))
				leftSide.append( (leftMat * mat).getPosition() )
				rightSide.append( (rightMat * mat).getPosition() )

		verts = [ (x,z) for x,y,z in leftSide ]
		verts.extend((x,z) for x,y,z in reversed(rightSide))

		PolygonArea.__init__(self,verts,offset)

	def __repr__(self):
		return "{}(points={}, radius={}, offset={})".format(self.__class__.__name__,self._path,self._radius,self._offset)

class CompositeShape(Shape):
	"""Shape composted of multiple shapes"""
	def __init__(self,shapes):
		self._shapes = list(shapes)

	def __repr__(self):
		return "{}(shapes={})".format(self.__class__.__name__,self._shapes)

	def containsPoint(self,point):
		"""Returns whether the point is inside the shape"""
		for shape in self._shapes:
			if shape.containsPoint(point):
				return True
		return False

	def createDebugNode(self,data):
		"""Create and return node object for visualizing proximity shape"""
		root = viz.addGroup()
		for shape in self._shapes:
			s = shape.createDebugNode(data)
			if s:
				s.setParent(root)
		return root

class Target(viz.Removable):
	"""A proximity target is the object that is detected by proximity sensors.
	The targets position is determined by the specified source object."""

	def __init__(self,source):
		self._source = createSource(source)

		# Remove self when source object is removed
		if isinstance(self.getSourceObject(),viz.Removable):
			self.getSourceObject().addRemoveCallback(self._notifyRemoveCallbacks)

	def __repr__(self):
		return "{}(source={})".format(self.__class__.__name__,self._source)

	def getSource(self):
		"""Return the source object of the target"""
		return self._source

	def getSourceObject(self):
		"""Return the underlying object of the target source"""
		return self._source.getObject()

	def getPosition(self):
		"""Get current position of target"""
		return self._source.getPosition()

class Sensor(viz.Removable):
	"""A proximity sensor is the object that detects when a target is within range.
	The area of the sensor is determined by the specified shape.
	The sensors position is determined by the specified source object."""

	def __init__(self,shape,source):
		"""@arg shape Shape()"""
		self._shape = shape
		self._source = createSource(source)

		# Remove self when source object is removed
		if isinstance(self.getSourceObject(),viz.Removable):
			self.getSourceObject().addRemoveCallback(self._notifyRemoveCallbacks)

	def __repr__(self):
		return "{}(shape={}, source={})".format(self.__class__.__name__,self._shape,self._source)

	def getShape(self):
		"""Return the shape object of the sensor"""
		return self._shape

	def getSource(self):
		"""Return the source object of the sensor"""
		return self._source

	def getSourceObject(self):
		"""Return the underlying object of the sensor source"""
		return self._source.getObject()

	def containsPoint(self,point):
		"""Return whether the sensor contains the specified point"""

		# Transform point into source reference frame
		m = self._source.getMatrix()
		m.invert()
		point_local = m.preMultVec(point)

		# Return whether point is inside shape
		return self._shape.containsPoint(point_local)

def addBoundingBoxSensor(node,name='',scale=(1.0,1.0,1.0)):
	"""Utility function for creating a proximity sensor using the bounding box of a node"""
	bb = node.getBoundingBox(viz.ABS_LOCAL,name)
	w,h,d = bb.size
	return Sensor(Box(size=[w*scale[0],h*scale[1],d*scale[2]],center=bb.center),node)

def addBoundingSphereSensor(node,name='',scale=1.0):
	"""Utility function for creating a proximity sensor using the bounding sphere of a node"""
	bs = node.getBoundingSphere(viz.ABS_LOCAL,name)
	return Sensor(Sphere(radius=bs.radius*scale,center=bs.center),node)

class Manager(viz.EventClass,viz.Removable):
	"""Manages a collection of proximity sensor and targets and
	automatically triggers events when a target enters/exits a sensor range"""

	def __init__(self, priority=DEFAULT_UPDATE_PRIORITY):
		viz.EventClass.__init__(self)

		self._sensors = {}
		self._targets = {}

		self._debugRoot = None
		self._debugColor = list(DEFAULT_DEBUG_COLOR)
		self._debugActiveColor = list(DEFAULT_DEBUG_ACTIVE_COLOR)

		self.callback(viz.UPDATE_EVENT,self._onUpdate,priority=priority)

	def _eventClassRemoved(self):
		self._notifyRemoveCallbacks()
		self._sensors.clear()
		self._targets.clear()
		if self._debugRoot:
			self._debugRoot.remove()
			self._debugRoot = None

	def _onUpdate(self,e):
		self.update()

	def remove(self):
		"""Remove the proximity manager"""
		self.unregister()

	def update(self):
		"""Update state of proximity sensors and trigger enter/exit events if needed"""

		# Don't bother checking if no targets or sensors
		if not (self._targets and self._sensors):
			return

		# Set of active sensors for debugging purposes
		activeSensors = None
		if self._debugRoot is not None:
			activeSensors = set()

		# Check if each target is in range of each sensor
		events = []
		for t,active in self._targets.iteritems():
			pos = t.getPosition()
			for s in self._sensors.iterkeys():
				isInside = s.containsPoint(pos)
				if isInside and activeSensors is not None:
					activeSensors.add(s)
				wasInside = s in active
				if wasInside != isInside:
					if isInside:
						active.add(s)
						events.append( (ENTER_PROXIMITY_EVENT, ProximityEvent(s,t,self)) )
					else:
						active.remove(s)
						events.append( (EXIT_PROXIMITY_EVENT, ProximityEvent(s,t,self)) )

		# Update debug nodes
		if self._debugRoot is not None:
			for sensor,data in self._sensors.iteritems():
				if data.debug:
					data.debug.setMatrix(sensor.getSource().getMatrix())
					isActive = sensor in activeSensors
					if isActive != data.debug.lastActive:
						data.debug.lastActive = isActive
						data.debug.color(self._debugActiveColor if isActive else self._debugColor)

		# Trigger events
		for id,e in events:
			viz.sendEvent(id,e)

	def _updateActiveDebugColor(self):
		"""Update color for active debug shapes"""
		for sensor,data in self._sensors.iteritems():
			if data.debug and data.debug.lastActive:
				data.debug.color(self._debugActiveColor)

	def _createSensorDebugNode(self,sensor,data):
		"""Create debug node for sensor"""
		node = sensor.getShape().createDebugNode(data)
		if node:
			node.setParent(self._debugRoot)
			sensor_data = self._sensors[sensor]
			if sensor_data.debug:
				sensor_data.debug.remove()
			sensor_data.debug = node
			sensor_data.debug.lastActive = False

	def setDebug(self,mode, parent = viz.WORLD, scene = viz.MainScene):
		"""Set whether debugging of proximity sensor shapes is enabled"""
		if mode == viz.TOGGLE:
			mode = not self.getDebug()

		if mode and self._debugRoot is None:

			# Create debug root node and shapes for all current sensors
			self._debugRoot = viz.addGroup(parent=parent,scene=scene)
			self._debugRoot.disable([viz.PICKING,viz.INTERSECTION])
			debugData = viz.Data(color=self._debugColor)
			for sensor in self._sensors.iterkeys():
				self._createSensorDebugNode(sensor,debugData)

		elif not mode and self._debugRoot is not None:

			# Remove debug root node and shapes for all current sensors
			self._debugRoot.remove()
			self._debugRoot = None
			for sensor,data in self._sensors.iteritems():
				data.debug = None

	def getDebug(self):
		"""Get whether debugging of proximity sensor shapes is enabled"""
		return self._debugRoot is not None

	def setDebugColor(self,color):
		"""Set the color for debug shapes"""
		self._debugColor = [color[0],color[1],color[2]]
		if self._debugRoot is not None:
			self._debugRoot.color(self._debugColor)
			self._updateActiveDebugColor()

	def getDebugColor(self):
		"""Get the color for debug shapes"""
		return list(self._debugColor)

	def setDebugActiveColor(self,color):
		"""Set the active color for debug shapes"""
		self._debugActiveColor = [color[0],color[1],color[2]]
		if self._debugRoot is not None:
			self._updateActiveDebugColor()

	def getDebugActiveColor(self):
		"""Get the active color for debug shapes"""
		return list(self._debugActiveColor)

	def getDebugNode(self):
		"""Get root node for proximity sensor debugger"""
		return self._debugRoot

	def addSensor(self,sensor):
		"""Add a proximity sensor to the manager"""
		if not sensor in self._sensors:
			self._sensors[sensor] = viz.Data(debug=None)
			sensor.addRemoveCallback(self.removeSensor,passObject=True)

			# Create debug node if debugging is enabled
			if self._debugRoot:
				debugData = viz.Data(color=self._debugColor)
				self._createSensorDebugNode(sensor,debugData)
		return sensor

	def removeSensor(self,sensor):
		"""Remove a proximity sensor from the manager"""
		try:
			data = self._sensors[sensor]
		except KeyError:
			return

		# Remove debug node of sensor
		if data.debug:
			data.debug.remove()
			
			# Remove sensor from target's active list
		for active in self._targets.itervalues():
			active.discard(sensor)

		# Remove sensor from dictionary
		del self._sensors[sensor]
		sensor.removeRemoveCallback(self.removeSensor)

	def clearSensors(self):
		"""Remove all proximity sensors from the manager"""
		sensors = list(self._sensors.iterkeys())
		for s in sensors:
			self.removeSensor(s)

	def getSensors(self):
		"""Get a list of proximity sensors"""
		return list(self._sensors.iterkeys())

	def addTarget(self,target):
		"""Add a proximity target to the manager"""
		if not target in self._targets:
			self._targets[target] = set()
			target.addRemoveCallback(self.removeTarget,passObject=True)
		return target

	def removeTarget(self,target):
		"""Remove a proximity target from the manager"""
		try:
			del self._targets[target]
		except KeyError:
			return

		target.removeRemoveCallback(self.removeTarget)

	def clearTargets(self):
		"""Remove all proximity targets from the manager"""
		targets = list(self._targets.iterkeys())
		for t in targets:
			self.removeTarget(t)

	def getTargets(self):
		"""Get a list of proximity targets"""
		return list(self._targets.iterkeys())

	def getActiveTargets(self,sensor=None):
		"""Get a list of targets that have activated the specified sensor since the last update"""
		if sensor is None:
			return [ t for t,active in self._targets.iteritems() if active ]
		return [ t for t,active in self._targets.iteritems() if sensor in active ]

	def getActiveSensors(self,target=None):
		"""Get a list of sensors that have been activated by the specified target since the last update"""
		if target is None:
			active = set()
			for a in self._targets.itervalues():
				active.update(a)
		else:
			active = self._targets.get(target,None)
		if active is not None:
			return list(active)
		return []

	def getSensorsContainingTarget(self,target):
		"""Get a list of sensors that contain the specified target"""
		return self.getSensorsContainingPoint(target.getPosition())

	def getSensorsContainingPoint(self,point):
		"""Get a list of sensors that contain the specified point"""
		return [ s for s in self._sensors.iterkeys() if s.containsPoint(point) ]

	def onEnter(self,sensor,func,*args,**kw):
		"""Call specified function when a target enters the proximity sensor"""
		if sensor is None:
			event = vizact.onevent(ENTER_PROXIMITY_EVENT,lambda e: (e.manager is self,e),func,*args,**kw)
		else:
			event = vizact.onevent(ENTER_PROXIMITY_EVENT,lambda e: (e.manager is self and e.sensor is sensor,e),func,*args,**kw)

		self.addRemoveCallback(event.remove)
		if isinstance(sensor,viz.Removable):
			sensor.addRemoveCallback(event.remove)

		return event

	def onExit(self,sensor,func,*args,**kw):
		"""Call specified function when a target exits the proximity sensor"""
		if sensor is None:
			event = vizact.onevent(EXIT_PROXIMITY_EVENT,lambda e: (e.manager is self,e),func,*args,**kw)
		else:
			event = vizact.onevent(EXIT_PROXIMITY_EVENT,lambda e: (e.manager is self and e.sensor is sensor,e),func,*args,**kw)

		self.addRemoveCallback(event.remove)
		if isinstance(sensor,viz.Removable):
			sensor.addRemoveCallback(event.remove)

		return event

class _waitProximityBase(viztask.Condition):
	"""Base class for proximity enter/exit conditions"""

	class _ProximityEventHandler(viz.EventClass):
		def __init__(self,eventID,sensor,target,manager,priority):
			viz.EventClass.__init__(self)
			self.callback(eventID,self._onProximity,priority=priority)

			self._sensors = viztask.Condition.Items(sensor)
			self._targets = viztask.Condition.Items(target)
			self._managers = viztask.Condition.Items(manager)

			self.data = None
			self.activated = False

		def _onProximity(self,e):
			"""@arg e ProximityEvent()"""
			if e.sensor in self._sensors and e.target in self._targets and e.manager in self._managers:
				self.data = e
				self.activated = True

	def __init__(self,sensor=None,target=None,manager=None,priority=0):
		"""sensor - A Sensor object, list of Sensor objects, or None to allow any sensor
		target - A Target object, list of Target objects, or None to allow any target
		manager - A Manager object, list of Manager objects, or None to allow any manager"""
		self._proximityHandler = self._ProximityEventHandler(self.PROXIMITY_EVENT,sensor,target,manager,priority)

	def __del__(self):
		self._proximityHandler.unregister()

	def reset(self):
		self._proximityHandler.data = None
		self._proximityHandler.activated = False

	def update(self):
		return self._proximityHandler.activated

	def getData(self):
		return self._proximityHandler.data

class waitEnter(_waitProximityBase):
	"""viztask condition that waits for a proximity sensor enter event"""
	PROXIMITY_EVENT = ENTER_PROXIMITY_EVENT

class waitExit(_waitProximityBase):
	"""viztask condition that waits for a proximity sensor exit event"""
	PROXIMITY_EVENT = EXIT_PROXIMITY_EVENT

if __name__ == '__main__':
	viz.go()
	viz.fov(60)
	viz.add('dojo.osgb')

	#Create proximity manager
	manager = Manager()
	manager.setDebug(True)

	#Add main viewpoint as proximity target
	target = Target(viz.MainView)
	manager.addTarget(target)

	#Create sphere sensor attached to static matrix
	sensor = Sensor(Sphere(1.0),source=viz.Matrix.translate(2,1.5,1))
	manager.addSensor(sensor)

	# Create composite sensor attached to a node
	group = viz.addGroup()
	group.setPosition(0,1.5,5)
	action = vizact.sequence( vizact.moveTo([-4,1.5,5],speed=1), vizact.moveTo([4,1.5,5],speed=1), viz.FOREVER)
	group.addAction( action)
	shapes = []
	shapes.append(Box([1,1,1]))
	shapes.append(Sphere(0.5,center=[0,1,0]))
	sensor = Sensor(CompositeShape(shapes),group)
	manager.addSensor(sensor)

	# Create box sensor attached to tracker
	tracker = viz.add('testtrack_all.dls')
	trackerLink = viz.link(tracker,viz.NullLinkable,offset=(0,1,0))
	sensor = Sensor(Box([0.5,0.5,0.5]),trackerLink)
	manager.addSensor(sensor)

	# Create sensor using bounding box of node
	node = viz.addChild('plant.osgb',pos=(8,0,6))
	node.addAction(vizact.spin(0,1,0,45,viz.FOREVER))
	sensor = addBoundingBoxSensor(node)
	manager.addSensor(sensor)

	# Create sensor using bounding sphere of node
	node = viz.addChild('beachball.osgb',pos=(-8,1.5,6))
	action = vizact.sequence( vizact.sizeTo([2,2,2],speed=1), vizact.sizeTo([1,1,1],speed=1), viz.FOREVER)
	node.addAction(action)
	sensor = addBoundingSphereSensor(node)
	manager.addSensor(sensor)

	# Create sensor using bounding box of sub-node
	node = viz.addChild('logo.ive',pos=(-4,0,7))
	action = vizact.sequence( vizact.moveTo([-4,1,7],speed=1), vizact.moveTo([-4,0,7],speed=1), viz.FOREVER)
	node.addAction(action)
	sensor = addBoundingBoxSensor(node,name='Sphere01-FACES')
	manager.addSensor(sensor)

	# Create sensor using avatar bone
	avatar = viz.addAvatar('vcc_male2.cfg',pos=[4, 0, 7],euler=[180,0,0])
	avatar.state(5)
	head = avatar.getBone('Bip01 Head')
	sensor = Sensor(Sphere(0.3,center=[0,0.1,0]),head)
	manager.addSensor(sensor)

	def EnterProximity(e):
		"""@args ProximityEvent()"""
		print 'entered',e.sensor

	def ExitProximity(e):
		"""@args ProximityEvent()"""
		print 'exited',e.sensor

	manager.onEnter(None,EnterProximity)
	manager.onExit(None,ExitProximity)

	vizact.onkeydown('d',manager.setDebug,viz.TOGGLE)
