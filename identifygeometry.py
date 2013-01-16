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

class identifyGeometry(QgsMapToolEmitPoint):
	def __init__(self, canvas):
		self.canvas = canvas
		QgsMapToolEmitPoint.__init__(self, canvas)
		QObject.connect( self, SIGNAL( "canvasClicked" ), self.onCanvasClicked )

	def canvasPressEvent(self, mouseEvent):
		point = self.toMapCoordinates( mouseEvent.pos() )
		self.emit( SIGNAL( "canvasClicked" ), point, mouseEvent.button(), mouseEvent.modifiers() )
		
	def onCanvasClicked(self, point, button, modifiers):
		layer = self.canvas.currentLayer()
		if layer == None:
			return
		if layer.type() != QgsMapLayer.VectorLayer:
			return
		if button != Qt.LeftButton:
			return
		point = self.canvas.mapRenderer().mapToLayerCoordinates(layer, point)
		pixTolerance = 6
		mapTolerance = pixTolerance * self.canvas.mapUnitsPerPixel()
		rect = QgsRectangle(point.x()-mapTolerance,point.y()-mapTolerance,point.x()+mapTolerance,point.y()+mapTolerance)

		provider = layer.dataProvider()
		provider.select([], rect, True, True)
		subset = []
		f = QgsFeature()
		while (provider.nextFeature(f)):
			subset.append(f)
		if len(subset) == 0:
			return
		if len(subset) > 1:
			idx = QgsSpatialIndex()
			for f in subset:
				idx.insertFeature(f)
			nearest = idx.nearestNeighbor( point, 1 )
			print nearest
			layer.featureAtId(nearest[0],f, True, False)
		self.emit( SIGNAL( "geomIdentified" ), layer, f)
