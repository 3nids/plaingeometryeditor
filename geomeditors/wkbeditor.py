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


class WkbEditor():
	def __init__(self, geomEditorDialog ):
		self.geomEditorDialog = geomEditorDialog
	
	def isGeomValid(self):
		return False
		
	def cursorPositionChanged(self):
		return
		
	def getGeom(self):
		return QgsGeometry()
