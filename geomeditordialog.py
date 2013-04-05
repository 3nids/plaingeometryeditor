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

try:
	from ui.ui_geomeditor import Ui_GeomEditor
except:
	from ui.ui_geomeditor_v18 import Ui_GeomEditor

from geomeditors.celleditor import CellEditor
from geomeditors.wkteditor import WktEditor
from geomeditors.wkbeditor import WkbEditor

from mysettings import mySettings, pluginName
from qgistools.pluginsettings import PluginSettings


class GeomEditorDialog(QDialog, Ui_GeomEditor, PluginSettings):
	def __init__(self,iface,layer,feature):
		self.iface = iface
		QDialog.__init__( self, iface.mainWindow() )
		self.setupUi(self)
		PluginSettings.__init__(self, pluginName, mySettings, False, True)
		
		self.setAttribute( Qt.WA_DeleteOnClose )
		self.feature = feature
		self.layer = layer
		self.initialGeom = QgsGeometry( feature.geometry() )
		self.modifiedGeom = QgsGeometry( feature.geometry()	)
		self.geomType = self.initialGeom.type()	
		self.cellEditor = CellEditor( self )
		self.wktEditor  = WktEditor(  self )
		self.wkbEditor  = WkbEditor(  self )
		if not self.geomType in (QGis.Point, QGis.Line, QGis.Polygon):
			self.close()
			return
		# qgis < 1.9
		# hide the geometry panel
		try:
			self.rubberSettingsFrame.setVisible(False)
		except:
			pass
		
		self.featureRubber = QgsRubberBand( iface.mapCanvas() )
		self.currentPointRubber = QgsRubberBand( iface.mapCanvas() )

		self.settings = MySettings(self)
		self.settings.settingChanged.connect(self.updateRubber)
		self.updateRubber(None)
			
			
		self.displayCombo.setCurrentIndex(1)

		# GUI stuff
		QObject.connect(self , SIGNAL( "finished(int)" ) , self.finish )
		QObject.connect(self.applyButton, SIGNAL( "clicked()" ) , self.applyGeometry )
		QObject.connect(self.sketchBox  , SIGNAL( "clicked()" ) , self.geomChanged )	
		QObject.connect(self.geomTextEdit, SIGNAL( "textChanged()" ) , self.geomChanged )
		QObject.connect(self.geomTextEdit, SIGNAL("cursorPositionChanged()"), self.getEditor().cursorPositionChanged )
		self.layerEditable()
		QObject.connect(layer, SIGNAL( "editingStopped() " ), self.layerEditable )
		QObject.connect(layer, SIGNAL( "editingStarted() " ), self.layerEditable )
		self.layerLabel.setText( layer.name() )
		try:
			featureTitle = feature.attribute( layer.displayField() ).toString()
			if featureTitle == "":
				featureTitle = "%s" % feature.id()
			self.featureEdit.setText( featureTitle )
		except: # qgis <1.9
			self.featureEdit.setText( "%s" % feature.id() )
			
		# write geometry in text edit
		self.getEditor().setGeom( self.initialGeom )


	def getEditor(self):
		idx = self.displayCombo.currentIndex()
		if idx == 0:
			return self.cellEditor
		elif idx == 1:
			return self.wktEditor
		elif idx == 2:
			return self.wkbEditor
		else:
			return None
			
	@pyqtSignature("on_displayCombo_currentIndexChanged(int)")
	def on_displayCombo_currentIndexChanged(self, idx):
		self.getEditor().setGeom( self.modifiedGeom )				

	def finish(self, state):
		self.featureRubber.reset()
		self.currentPointRubber.reset()
		QObject.disconnect(self.layer, SIGNAL( "editingStarted()" ), self.layerEditable )
		QObject.disconnect(self.layer, SIGNAL( "editingStopped()" ), self.layerEditable )
		self.close()

	@pyqtSignature("on_resetButton_clicked()")
	def on_resetButton_clicked(self):
		self.getEditor().setGeom( self.initialGeom )

	@pyqtSignature("on_copyButton_clicked()")
	def on_copyButton_clicked(self):
		QApplication.clipboard().setText( self.geomTextEdit.toPlainText() )

	def layerEditable(self):	
		layerIsEditable = self.layer.isEditable()
		self.geomTextEdit.setEnabled( layerIsEditable )
		self.resetButton.setEnabled( layerIsEditable )
		self.applyButton.setEnabled( layerIsEditable )	

	def geomChanged(self):
		self.featureRubber.reset()
		editor = self.getEditor()
		if editor.isGeomValid():
			bgColor = "white"
			self.modifiedGeom = editor.getGeom()
			self.displayCombo.setEnabled( True )
			self.applyButton.setEnabled( self.layer.isEditable() )
			geomStatus = "Geometry is valid"
			if self.sketchBox.isChecked():
				self.featureRubber.setToGeometry( self.modifiedGeom , self.layer )
		else:
			bgColor = "red"
			self.applyButton.setEnabled( False )
			self.displayCombo.setEnabled( False )
			geomStatus = "invalid"

		p = self.geomTextEdit.palette()
		p.setColor( QPalette.Base, QColor( bgColor ) )
		self.geomTextEdit.setPalette(p)
		self.geomStatusLabel.setText( geomStatus )

	def cursorPositionChanged( self, curPos, richText ):
		QObject.disconnect(self.geomTextEdit, SIGNAL( "textChanged()" ) , self.geomChanged) # textEdited signal does not exist yet, so need to disconnect
		QObject.disconnect(self.geomTextEdit, SIGNAL("cursorPositionChanged()"), self.getEditor().cursorPositionChanged )
		self.geomTextEdit.setText(richText)
		cursor = self.geomTextEdit.textCursor()
		cursor.setPosition( curPos )
		self.geomTextEdit.setTextCursor( cursor )
		QObject.connect(self.geomTextEdit, SIGNAL( "textChanged()" ) , self.geomChanged)
		QObject.connect(self.geomTextEdit, SIGNAL("cursorPositionChanged()"), self.getEditor().cursorPositionChanged )
		
	def currentPointChanged( self, point ):
		self.currentPointRubber.setToGeometry( point , self.layer )
		
	def applyGeometry(self):
		geometry = self.getEditor().getGeom()
		if geometry:
			self.layer.changeGeometry( self.feature.id(), geometry )
			self.iface.mapCanvas().refresh()
			self.close()
			
	def updateRubber(self, setting):
		self.featureRubber.setColor(self.settings.value("rubberColor"))
		
		
		self.currentPointRubber.setWidth(10)
		try:
			self.currentPointRubber.setIconSize(10)
		except:
			pass
		
		self.iface.mapCanvas().refresh()
