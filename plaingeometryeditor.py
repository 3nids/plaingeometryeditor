from __future__ import absolute_import
from builtins import object
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
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon, QDesktopServices

from .gui.identifygeometry import IdentifyGeometry
from .gui.geomeditordialog import GeomEditorDialog

import resources


class PlainGeometryEditor(object):

    def __init__(self, iface):
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()
        self.dlgs = []
   
    def initGui(self):
        # help
        self.helpAction = QAction(QIcon(":/help.svg"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://3nids.github.io/plaingeometryeditor")))
        self.iface.addPluginToMenu("&Plain Geometry Editor", self.helpAction)
        # map tool action
        self.mapToolAction = QAction(QIcon(":/icon1.svg"),
                                     "Plain Geometry Editor", self.iface.mainWindow())
        self.mapToolAction.setCheckable(True)
        self.mapTool = IdentifyGeometry(self.mapCanvas)
        self.mapTool.geomIdentified.connect(self.editGeometry)
        self.mapTool.setAction(self.mapToolAction)
        self.mapToolAction.triggered.connect(self.setMapTool)
        self.iface.addToolBarIcon(self.mapToolAction)
        self.iface.addPluginToMenu("&Plain Geometry Editor", self.mapToolAction)

    def unload(self):
        self.iface.removePluginMenu("&Plain Geometry Editor", self.helpAction)
        self.iface.removePluginMenu("&Plain Geometry Editor", self.mapToolAction)
        self.iface.removeToolBarIcon(self.mapToolAction)

    def setMapTool(self):
        self.mapCanvas.setMapTool(self.mapTool)
        
    def editGeometry(self, layer, feature):
        dlg = GeomEditorDialog(layer, feature, self.mapCanvas, self.iface.mainWindow())
        dlg.show()
        # save dlg so it does not get out of scope and layer is properly disconnect
        self.dlgs.append(dlg)

