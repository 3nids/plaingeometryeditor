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

from ui_geomeditor import Ui_GeomEditor

class geomEditor(QDialog, Ui_GeomEditor ):
	def __init__(self,iface):
		self.iface = iface
		QDialog.__init__(self)
		self.setupUi(self)
		self.setWindowFlags( Qt.WindowStaysOnTopHint )
		QObject.connect(self , SIGNAL( "finished(int)" ) , self.finish)
		QObject.connect(self.applyButton , SIGNAL( "clicked()" ) , self.applyGeometry)
		QObject.connect(self.wktText , SIGNAL( "textChanged()" ) , self.geomChanged)
		QObject.connect(self.sketchBox , SIGNAL( "clicked()" ) , self.geomChanged)	
		self.newRubber = QgsRubberBand(  iface.mapCanvas() )
	
	def setup(self, layer, feature):	
		self.feature = feature
		self.layer = layer
		self.initGeom = feature.geometry()
		self.layerEditable()
		QObject.connect(layer, SIGNAL( "editingStarted() " ), self.layerEditable )
		QObject.connect(layer, SIGNAL( "editingStopped() " ), self.layerEditable )
		self.wktText.setText( self.initGeom.exportToWkt() )
		
	def finish(self, state):
		self.newRubber.reset()
		QObject.disconnect(self.layer, SIGNAL( "editingStarted() " ), self.layerEditable )
		QObject.disconnect(self.layer, SIGNAL( "editingStopped() " ), self.layerEditable )

	@pyqtSignature("on_resetButton_clicked()")
	def on_resetButton_clicked(self):
		self.wktText.setText( self.initGeom.exportToWkt() )
		
	def layerEditable(self):	
		layerIsEditable = self.layer.isEditable()
		self.wktText.setEnabled( layerIsEditable )
		self.resetButton.setEnabled( layerIsEditable )
		self.applyButton.setEnabled( layerIsEditable )	

	def geomChanged(self):
		self.newRubber.reset()
		geoText = self.wktText.toPlainText()
		geometry = QgsGeometry.fromWkt( unicode( geoText ) )
		if not geometry:
			self.applyButton.setEnabled( False )
			bgColor = "red"
		else:
			if self.layer.isEditable():
				self.applyButton.setEnabled( True )
			if self.sketchBox.isChecked():
				self.newRubber.addGeometry( geometry, self.layer )
			bgColor = "white"
		p = self.wktText.palette()
		p.setColor( QPalette.Base, QColor( bgColor ) );
		self.wktText.setPalette(p)
		#QObject.disconnect(self.wktText , SIGNAL( "textChanged()" ) , self.geomChanged) # textEdited signal does not exist yet, so need to disconnect
		#self.wktText.setText("<font style=\"BACKGROUND-COLOR: "+bgColor+"\">"+geoText+"</font>") 
		#QObject.connect(self.wktText , SIGNAL( "textChanged()" ) , self.geomChanged)

	def applyGeometry(self):
		geometry = QgsGeometry.fromWkt( unicode( self.wktText.toPlainText() ) )
		if geometry:
			self.layer.changeGeometry( self.feature.id(), geometry )
			self.iface.mapCanvas().refresh()
