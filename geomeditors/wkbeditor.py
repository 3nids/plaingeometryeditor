from __future__ import absolute_import
from builtins import str
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
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QTextEdit
from qgis.core import QgsGeometry

from .geomeditor import GeomEditor

import binascii

SRID_FLAG = 0x20000000


class WkbEditor(QTextEdit, GeomEditor):
    currentPointChanged = pyqtSignal(QgsGeometry)
    geometryChanged = pyqtSignal(QgsGeometry)

    def __init__(self, layer, geometry, parent=None):
        GeomEditor.__init__(self, layer, geometry)
        QTextEdit.__init__(self, parent)

        self.setGeom(geometry)
        self.textChanged.connect(self.geomChanged)
        self.layerEditable()

    def getGeom(self):
            geoText = str(self.toPlainText())
            geom = self.wkb2qgis(geoText)
            if geom.isGeosValid():
                return geom
            else:
                return None

    def setGeom(self, geometry):
        hexText = binascii.b2a_hex(geometry.asWkb())
        self.setText(hexText)

    def layerEditable(self):
        layerIsEditable = self.layer.isEditable()
        self.setReadOnly(not layerIsEditable)

    def geomChanged(self):
        geom = self.getGeom()
        if geom is None:
            geom = QgsGeometry()
        self.geometryChanged.emit(geom)

    def wkb2qgis(self, wkb):
        geom = QgsGeometry()
        try:
            geomType = int("0x" + self.decodeBinary(wkb[2:10]), 0)
            if geomType & SRID_FLAG:
                wkb = wkb[:2] + self.encodeBinary(geomType ^ SRID_FLAG) + wkb[18:]
            geom.fromWkb(binascii.a2b_hex(wkb))
        except TypeError:
            pass
        return geom

    def encodeBinary(self, value):
        # https://github.com/elpaso/quickwkt/blob/master/QuickWKT.py#L132
        wkb = binascii.a2b_hex("%08x" % value)
        wkb = wkb[::-1]
        wkb = binascii.b2a_hex(wkb)
        return wkb

    def decodeBinary(self, wkb):
        """Decode the binary wkb and return as a hex string"""
        value = binascii.a2b_hex(wkb)
        value = value[::-1]
        value = binascii.b2a_hex(value)
        return value
