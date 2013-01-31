"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2013
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *


class GeomEditor():
	def __init__(self,geomType):
		self.geomType = geomType
	
	def isGeomValid(self):
		return False
		
	def cursorPositionChanged(self):
		return
		
	def getGeom(self):
		return QgsGeometry()
