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
	from qgis.gui import QgsMapToolIdentify 
except:
	from qgis.gui import QgsMapTool as QgsMapToolIdentify 	

class identifyGeometry(QgsMapToolIdentify):
	def __init__(self, canvas):
		self.canvas = canvas
		QgsMapToolIdentify.__init__(self, canvas)

	def canvasReleaseEvent(self, mouseEvent):
		if hasattr(self,"identify"):
			if self.identify(mouseEvent.x(),mouseEvent.y(), self.TopDownStopAtFirst, self.VectorLayer):
				result = self.results().mVectorResults[0]
				self.emit( SIGNAL( "geomIdentified" ), result.mLayer, result.mFeature)
		else:
			point = self.toMapCoordinates( mouseEvent.pos() )
			layer = self.canvas.currentLayer()
			if layer == None:
				return
			if layer.type() != QgsMapLayer.VectorLayer:
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
			
			
		
