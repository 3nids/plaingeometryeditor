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

from identifygeometry import IdentifyGeometry
from geomeditordialog import GeomEditorDialog

import resources

class PlainGeometryEditor():

	def __init__(self, iface):
		self.iface = iface
	
	def initGui(self):
		self.mapToolAction = QAction(QIcon(":/plugins/plaingeometryeditor/icons/plaingeometryeditor-32.png"), "Plain Geometry Editor", self.iface.mainWindow())
		self.mapToolAction.setCheckable(True)
		QObject.connect(self.mapToolAction, SIGNAL("triggered()"), self.mapToolInit)
		self.iface.addToolBarIcon(self.mapToolAction)
		self.iface.addPluginToMenu("&Plain Geometry Editor", self.mapToolAction)
				
	def unload(self):
		self.iface.removePluginMenu("&Plain Geometry Editor",self.mapToolAction)
		self.iface.removeToolBarIcon(self.mapToolAction)
		
	def mapToolInit(self):
		canvas = self.iface.mapCanvas()
		if self.mapToolAction.isChecked() is False:
			canvas.unsetMapTool(self.mapTool)
			return
		self.mapToolAction.setChecked( True )
		self.mapTool = IdentifyGeometry(canvas)
		QObject.connect(self.mapTool , SIGNAL("geomIdentified") , self.editGeometry ) 
		canvas.setMapTool(self.mapTool)
		QObject.connect( canvas, SIGNAL( "mapToolSet(QgsMapTool *)" ), self.mapToolChanged)
		
	def mapToolChanged(self, tool):
		QObject.disconnect( self.iface.mapCanvas(), SIGNAL( "mapToolSet(QgsMapTool *)" ), self.mapToolChanged)
		self.mapToolAction.setChecked( False )
		self.iface.mapCanvas().unsetMapTool(self.mapTool)
		
	def editGeometry(self, layer, feature):
		dlg = GeomEditorDialog(self.iface, layer, feature)
		dlg.show()

