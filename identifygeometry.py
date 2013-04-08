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

class IdentifyGeometry(QgsMapToolIdentify):
	def __init__(self, canvas):
		self.canvas = canvas
		QgsMapToolIdentify.__init__(self, canvas)
		#self.setCursor( QCursor( QPixmap( self.cursorPixmap() ) , 1 , 1 ) )

	def canvasReleaseEvent(self, mouseEvent):
		results = self.identify(mouseEvent.x(),mouseEvent.y(), self.TopDownStopAtFirst, self.VectorLayer)
		if len(results) > 0:
			self.emit( SIGNAL( "geomIdentified" ), results[0].mLayer, results[0].mFeature)
			
			
	def cursorPixmap(self):
		return {
		  "28 16 3 1",                     
		  "# c None",                      
		  "a c #000000",                   
		  ". c #ffffff",                   
		  ".###########################",  
		  "...#################..######",  
		  ".aa..############...aa...###",  
		  "#.aaa..#########.aaaaaaaa.##",  
		  "#.aaaaa..######.aa......aa.#",  
		  "##.aaaaaa..###.a..######..##",  
		  "##.aaaaaa.###.a.#####......#",  
		  "##.aaaaa.####.a.#####.aaaaa.",  
		  "###.aaaaa.###.a.#####.aaaaa.",  
		  "###.aa.aaa.###.a..####...aa.",  
		  "####..#..aa.###.aa......aa.#",  
		  "####.####.aa.###.aaaaaaaa.##",  
		  "##########.aa..##...aa...###",  
		  "###########.aa..####..######",  
		  "############.a.#############",  
		  "#############.##############"   
		}		
