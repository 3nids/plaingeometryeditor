#-----------------------------------------------------------
#
# Plain Geometry Editor is a QGIS plugin to edit geometries
# using plain text editors (WKT, WKB)
#
# Copyright    : (C) 2013 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import re


class WktEditor():
    def __init__(self, geomEditorDialog):
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
            raise NameError("No geometry found")

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
        geometry = QgsGeometry.fromWkt(unicode(geoText))
        if not geometry:
            return False
        else:
            return True

    def setGeom(self, geometry):
          print geometry.exportToWkt()
          self.geomEditorDialog.geomTextEdit.setText(geometry.exportToWkt())

    def getGeom(self):
        if self.isGeomValid():
            geoText = self.geomEditorDialog.geomTextEdit.toPlainText()
            geometry = QgsGeometry.fromWkt(unicode(geoText))
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
            if self.inPointReg.match(geoText[curPos]):
                ml = self.leftPointDelimiter.search(geoText[:curPos])
                mr = self.rightPointDelimiter.match(geoText[curPos:])
                #print ml,geoText[:curPos]
                #print mr,geoText[curPos:]
                if ml and mr:
                    l = ml.start()+1
                    r = curPos+mr.end()-1
                    pointText = geoText[l:r]
                    #print l,r,pointText

                    highlight = QTextEdit.ExtraSelection()
                    highlight.cursor = self.geomEditorDialog.geomTextEdit.textCursor()
                    highlight.cursor.setPosition(l)
                    highlight.cursor.setPosition(r, QTextCursor.KeepAnchor)
                    highlight.format.setBackground(Qt.green)
                    extras = [ highlight ]
                    self.geomEditorDialog.geomTextEdit.setExtraSelections(extras)

                    mm = self.spacePointReg.match(pointText)
                    if mm:
                        x = float(pointText[:mm.end()])
                        y = float(pointText[mm.end():])
                        currPointGeom = QgsGeometry.fromPoint(QgsPoint(x, y))
                        #print "point ",x,y
        self.geomEditorDialog.currentPointChanged(currPointGeom)
