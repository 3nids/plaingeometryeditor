"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2013
"""


# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from identifygeometry import identifyGeometry
from geomeditor import geomEditor

import resources

class PlainGeometryEditor():

	def __init__(self, iface):
		self.iface = iface
	
	def initGui(self):
		self.geomEditAction = QAction(QIcon(":/plugins/plaingeometryeditor/icons/plaingeometryeditor-32.png"), "Edit geometry", self.iface.mainWindow())
		self.geomEditAction.setCheckable(True)
		QObject.connect(self.geomEditAction, SIGNAL("triggered()"), self.geomEditInitTool)
		self.iface.addToolBarIcon(self.geomEditAction)
		self.iface.addPluginToMenu("&WKT Edit", self.geomEditAction)
				
	def unload(self):
		self.iface.removePluginMenu("&WKT Edit",self.geomEditAction)
		self.iface.removeToolBarIcon(self.geomEditAction)
		
	def geomEditInitTool(self):
		canvas = self.iface.mapCanvas()
		if self.geomEditAction.isChecked() is False:
			canvas.unsetMapTool(self.geomEdit)
			return
		self.geomEditAction.setChecked( True )
		self.geomEdit = identifyGeometry(canvas)
		QObject.connect(self.geomEdit , SIGNAL("geomIdentified") , self.editGeometry ) 
		canvas.setMapTool(self.geomEdit)
		QObject.connect( canvas, SIGNAL( "mapToolSet(QgsMapTool *)" ), self.mapToolChanged)
		
	def mapToolChanged(self, tool):
		QObject.disconnect( self.iface.mapCanvas(), SIGNAL( "mapToolSet(QgsMapTool *)" ), self.mapToolChanged)
		self.geomEditAction.setChecked( False )
		self.iface.mapCanvas().unsetMapTool(self.geomEdit)
		
	def editGeometry(self, layer, feature):
		dlg = geomEditor(self.iface, layer, feature)
		dlg.exec_()
