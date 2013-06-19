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

from PyQt4.QtGui import QAction, QIcon

from gui.identifygeometry import IdentifyGeometry
from gui.geomeditordialog import GeomEditorDialog

import resources


class PlainGeometryEditor():

    def __init__(self, iface):
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()
   
    def initGui(self):
        self.mapToolAction = QAction(QIcon(":/plugins/plaingeometryeditor/icons/plaingeometryeditor-32.png"),
                                     "Plain Geometry Editor", self.iface.mainWindow())
        self.mapToolAction.setCheckable(True)
        self.mapToolAction.triggered.connect(self.mapToolInit)
        self.iface.addToolBarIcon(self.mapToolAction)
        self.iface.addPluginToMenu("&Plain Geometry Editor", self.mapToolAction)
                  
    def unload(self):
        self.iface.removePluginMenu("&Plain Geometry Editor", self.mapToolAction)
        self.iface.removeToolBarIcon(self.mapToolAction)
        
    def mapToolInit(self):
        canvas = self.mapCanvas
        if self.mapToolAction.isChecked() is False:
            canvas.unsetMapTool(self.mapTool)
            return
        self.mapToolAction.setChecked(True)
        self.mapTool = IdentifyGeometry(canvas)
        self.mapTool.geomIdentified.connect(self.editGeometry)
        canvas.setMapTool(self.mapTool)
        canvas.mapToolSet.connect(self.mapToolChanged)
        
    def mapToolChanged(self, tool):
        self.mapCanvas.mapToolSet.disconnect(self.mapToolChanged)
        self.mapToolAction.setChecked(False)
        self.mapCanvas.unsetMapTool(self.mapTool)
        
    def editGeometry(self, layer, feature):
        dlg = GeomEditorDialog(layer, feature, self.mapCanvas, self.iface.mainWindow())
        dlg.show()

