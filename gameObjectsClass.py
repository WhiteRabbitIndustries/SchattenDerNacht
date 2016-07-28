#file  -- gameObjectsClass.py --
import xml.etree.ElementTree as ET

foldername = "audiofiles/"

class GameData:
	def __init__(self,xmlSource):
  		self.tree = ET.parse(xmlSource)
		self.root = self.tree.getroot()
		
		self.locationCount = 0
		self.locationList = []	
		for location in self.root.findall('location'):
			id = int(location.find('id').text)
			name = location.find('name').text
			coord = {'x': float(location.find('gpsX').text), 'y': float(location.find('gpsY').text)}

			wifiAPs = []
			for AP in location.find('wifi').findall('AP'):
				wifiAPs.append({'address': AP.find('address').text,'quality': int(AP.find('quality').text)})

			beacons = []
			for beacon in location.findAll('beacon'):
				beacons.append({'uuid': beacon.find('uuid').text,'rssi': int(beacon.find('rssi').text)})
			

			radius = int(location.find('radius').text)        
			self.locationList.append(GameLocation(id,name,coord,wifiAPs,radius,location))
			self.locationCount+=1

		#self.currentLocation = 1
		self.locationList[0].active = True

	def getLocationCount(self):
		return self.locationCount
		pass

class GameLocation:
	def __init__(self,id,name,coord,wifiAPs,radius,location, beaconsbeacons):
		self.id = id
		self.name = name
		self.coord = coord
		self.wifiAPs = wifiAPs
		self.radius = radius
		self.beacons = beacons

		#location conditions:
		self.active = False
		self.onloc = False
		#self.unlocked = False
		self.stateList = []
		self.statecount = 0
		for state in location.findall('state'):
			id = state.find('id').text
			self.stateList.append(LocationState(id,state))
			self.statecount+=1
		self.currentState = 0

	def getStateCount(self):
		return self.statecount
		pass



class LocationState:
	def __init__(self,id,state):
		self.id = id
		self.activated = False
		
		self.unlocklist = []
		#print self.id
		filename = state.find('audio').find('filename').text
		#print filename
		self.audiofile = foldername + filename

		if state.find('unlock') != None:
			#print "unlock found on %s" % id
			for location in state.find('unlock').findall('location'):
				locid = int(location.find('id').text)
				#print locid
				self.unlocklist.append(locid)
		else:
			pass
			#print "no unlocking"









"""
>>> root.tag
'data'
>>> root.attrib {}

>>> for child in root:
...     print child.tag, child.attrib
...
country {'name': 'Liechtenstein'}
country {'name': 'Singapore'}
country {'name': 'Panama'}
>>> root[0][1].text
'2008'


>>> for country in root.findall('country'):
...     rank = country.find('rank').text
...     name = country.get('name')
...     print name, rank
...



"""