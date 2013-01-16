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
	def __init__(self,iface,layer,feature):
		self.iface = iface
		self.feature = feature
		self.layer = layer
		QDialog.__init__(self)
		self.setupUi(self)
		
		self.initGeom = feature.geometry()
		self.wktText.setText( self.initGeom.exportToWkt() )
		
		QObject.connect(self , SIGNAL( "finished(int)" ) , self.deleteRubber)
		QObject.connect(self.resetButton , SIGNAL( "clicked()" ) , self.reset)
		QObject.connect(self.applyButton , SIGNAL( "clicked()" ) , self.applyGeometry)
		QObject.connect(self.wktText , SIGNAL( "textChanged()" ) , self.geomChanged)
		QObject.connect(self.sketchBox , SIGNAL( "clicked()" ) , self.geomChanged)
		
		if not layer.isEditable():
			self.wktText.setEnabled( False )
			self.resetButton.setEnabled( False )
			self.applyButton.setEnabled( False )

		# rubberbands
		self.initRubber = QgsRubberBand( iface.mapCanvas() )
		self.newRubber = QgsRubberBand(  iface.mapCanvas() )
		self.initRubber.setColor( Qt.red )
		self.newRubber.setColor( Qt.blue )
		self.initRubber.addGeometry( self.initGeom, layer )
		self.newRubber.addGeometry(  self.initGeom, layer )
		
	def deleteRubber(self, state):
		self.initRubber.reset()
		self.newRubber.reset()
		
	def reset(self):
		self.wktText.setText( self.initGeom.exportToWkt() )
		
	def geomChanged(self):
		self.newRubber.reset()
		geometry = QgsGeometry.fromWkt( unicode( self.wktText.toPlainText() ) )
		if not geometry:
			self.validityStatusLabel.setText( "invalid geometry" )
			self.applyButton.setEnabled( False )
		else:
			self.validityStatusLabel.setText( "valid geometry" )
			if self.layer.isEditable():
				self.applyButton.setEnabled( True )
			if self.sketchBox.isChecked():
				self.newRubber.addGeometry( geometry, self.layer )

	def applyGeometry(self):
		geometry = QgsGeometry.fromWkt( unicode( self.wktText.toPlainText() ) )
		if geometry:
			self.layer.changeGeometry( self.feature.id(), geometry )
