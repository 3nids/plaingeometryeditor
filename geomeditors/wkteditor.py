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

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QTextCursor, QTextEdit
from qgis.core import QgsGeometry, QgsPoint

from geomeditor import GeomEditor

# Regular expressions to detect the point in the WKT
import re
# Character in a point
# a point, a digit or a white space
inPointReg = re.compile("(-|\d|\s|\.)")
# Right delimiter of a point
# i.e. comma or right parenthesis some digits or not, eventually a point plus some digits,
# eventually some space plus a number and finally a comma or a right parenthesis
# dont forget it can start with a point!
rightPointDelimiter = re.compile("-?\d*(\.\d+)?(\s+-?\d+(\.\d+)?)?(,|\))")
# Left delimiter of a point
# i.e. a comma or a left parenthesis, some digits or not, eventually a point plus some digits,
# eventually some space plus a number and the end of string
# dont forget it can end by a point!
leftPointDelimiter = re.compile("(,|\()\s*-?\d+(\.\d*)?(\s+-?\d+(\.\d*)?)?$")
 # Look for middle space separator of a point
spacePointReg = re.compile("\s*-?\d+(\.\d+)?\s+")


class WktEditor(QTextEdit, GeomEditor):
    currentPointChanged = pyqtSignal(QgsGeometry)
    geometryChanged = pyqtSignal(QgsGeometry)

    def __init__(self, layer, feature, parent=None):
        GeomEditor.__init__(self, layer, feature)
        QTextEdit.__init__(self, parent)

        self.setGeom(feature.geometry())

        self.cursorPositionChanged.connect(self.emitCurrentPoint)
        self.textChanged.connect(self.geomChanged)

    def getGeom(self):
        try:
            geoText = self.toPlainText()
            return QgsGeometry().fromWkt(unicode(geoText))
        except:
            return None

    def setGeom(self, geometry):
        self.setText(geometry.exportToWkt())

    def layerEditable(self):
        layerIsEditable = self.layer.isEditable()
        self.setReadOnly(not layerIsEditable)

    def geomChanged(self):
        self.geometryChanged.emit(self.getGeom())

    def emitCurrentPoint(self):
        geoText = self.toPlainText()
        cursor = self.textCursor()
        curPos = cursor.position()
        curAnc = cursor.anchor()

        # Determine current point
        currPointGeom = QgsGeometry()
        self.setExtraSelections([])
        if self.isGeomValid() and 0 <= curPos < len(geoText):
            if inPointReg.match(geoText[curPos]):
                ml = leftPointDelimiter.search(geoText[:curPos])
                mr = rightPointDelimiter.match(geoText[curPos:])
                #print ml,geoText[:curPos]
                #print mr,geoText[curPos:]
                if ml and mr:
                    l = ml.start()+1
                    r = curPos+mr.end()-1
                    pointText = geoText[l:r]
                    #print l,r,pointText

                    highlight = self.ExtraSelection()
                    highlight.cursor = self.textCursor()
                    highlight.cursor.setPosition(l)
                    highlight.cursor.setPosition(r, QTextCursor.KeepAnchor)
                    highlight.format.setBackground(Qt.green)
                    extras = [highlight]
                    self.setExtraSelections(extras)

                    mm = spacePointReg.match(pointText)
                    if mm:
                        x = float(pointText[:mm.end()])
                        y = float(pointText[mm.end():])
                        currPointGeom = QgsGeometry().fromPoint(QgsPoint(x, y))
                        #print "point ",x,y
        self.currentPointChanged.emit(currPointGeom)
