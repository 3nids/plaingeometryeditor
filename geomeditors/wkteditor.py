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

import re

class WktEditor():
	def __init__(self, geomEditorDialog ):
		self.geomEditorDialog = geomEditorDialog
		if self.geomEditorDialog.geomType == QGis.Point:
			self.wktReg = re.compile("\s*point\s*\(\s*-?\d+(\.\d+)?\s+-?\d+(\.\d+)?\s*\)\s*$", re.IGNORECASE)
			print "Point"
		elif self.geomEditorDialog.geomType == QGis.Line:
			self.wktReg = re.compile("\s*linestring\s*\((\s*-?\d+(\.\d+)?\s+-?\d+(\.\d+)?\s*,)+\s*-?\d+(\.\d+)?\s+-?\d+(\.\d+)?\s*\)\s*$", re.IGNORECASE)
			print "Line"
		elif self.geomEditorDialog.geomType == QGis.Polygon:
			self.wktReg = re.compile("\s*polygon\s*\(\s*\((\s*-?\d+(\.\d+)?\s+-?\d+(\.\d+)?\s*,){2,}\s*-?\d+(\.\d+)?\s+-?\d+(\.\d+)?\s*\)\s*\)\s*$", re.IGNORECASE)
			print "Polygon"
		else:
			raise NameError( "No geometry found" )

		# Character in a point
		# a point, a digit or a white space
		self.inPointReg = re.compile("(-|\d|\s|\.)")

		# Right delimiter of a point, i.e. comma or right parenthesis
		# some digits or not, eventually a point plus some digits, eventually some space plus a number and finally a comma or a right parenthesis
		# dont forget it can start with a point!
		self.rightPointDelimiter = re.compile("-?\d*(\.\d+)?(\s+-?\d+(\.\d+)?)?(,|\))")

		# Left delimiter of a point, i.e. comma or left parenthesis
		# a comma or a left parenthesis, some digits or not, eventually a point plus some digits, eventually some space plus a number and the end of string
		# dont forget it can end by a point!
		self.leftPointDelimiter  = re.compile("(,|\()\s*-?\d+(\.\d*)?(\s+-?\d+(\.\d*)?)?$")

		# Look for middle space separator of a point
		self.spacePointReg = re.compile("\s*-?\d+(\.\d+)?\s+")

	def isGeomValid(self):
		geoText = self.geomEditorDialog.geomTextEdit.toPlainText()
		if not self.wktReg.match(geoText):
			return False
		geometry = QgsGeometry.fromWkt( unicode( geoText ) )
		if not geometry:
			return False
		else:
			return True

	def setGeom(self, geometry):
		print geometry.exportToWkt()
		self.geomEditorDialog.geomTextEdit.setText( geometry.exportToWkt() )

	def getGeom(self):
		if self.isGeomValid():
			geoText = self.geomEditorDialog.geomTextEdit.toPlainText()
			geometry = QgsGeometry.fromWkt( unicode( geoText ) )
			return geometry
		else:
			return QgsGeometry()

	def cursorPositionChanged(self):
		geoText = self.geomEditorDialog.geomTextEdit.toPlainText()
		cursor = self.geomEditorDialog.geomTextEdit.textCursor()
		curPos = cursor.position()
		curAnc = cursor.anchor()

		# Determine current point
		currPointGeom = QgsGeometry()
		if self.isGeomValid() and curPos < len(geoText) and curPos >= 0:
			if self.inPointReg.match( geoText[curPos] ):
				ml = self.leftPointDelimiter.search( geoText[:curPos] )
				mr = self.rightPointDelimiter.match( geoText[curPos:] )
				#print ml,geoText[:curPos]
				#print mr,geoText[curPos:]
				if ml and mr:
					l = ml.start()+1
					r = curPos+mr.end()-1
					pointText = geoText[l:r]
					#print l,r,pointText

					highlight = QTextEdit.ExtraSelection()
					highlight.cursor = self.geomEditorDialog.geomTextEdit.textCursor()
					highlight.cursor.setPosition( l )
					highlight.cursor.setPosition( r, QTextCursor.KeepAnchor )
					highlight.format.setBackground( Qt.green )
					extras = [ highlight ]
					self.geomEditorDialog.geomTextEdit.setExtraSelections( extras )

					mm = self.spacePointReg.match( pointText )
					if mm:
						x = pointText[:mm.end()].toDouble()[0]
						y = pointText[mm.end():].toDouble()[0]
						currPointGeom = QgsGeometry.fromPoint( QgsPoint( x, y ) )
						#print "point ",x,y
		self.geomEditorDialog.currentPointChanged( currPointGeom )
