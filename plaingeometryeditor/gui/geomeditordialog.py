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

import os
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import QGridLayout, QDialog
from qgis.PyQt.uic import loadUiType
from qgis.core import QgsGeometry, QgsWkbTypes
from qgis.gui import QgsRubberBand

from ..qgissettingmanager import *
from ..core.mysettings import MySettings
from ..geomeditors import GeomEditor, CellEditor, WkbEditor, WktEditor

Ui_GeomEditor, _ = loadUiType(os.path.join(os.path.dirname(__file__), '../ui/geomeditor.ui'))


class GeomEditorDialog(QDialog, Ui_GeomEditor, SettingDialog):
    def __init__(self, layer, feature, mapCanvas, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, setting_manager=self.settings, mode=UpdateMode.WidgetUpdate)
        self.mapCanvas = mapCanvas
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.feature = feature
        self.initialGeometry = QgsGeometry(feature.geometry())
        self.layer = layer
        self.init_widgets()
        
        # close if no geom, hide "sketch current point" if not needed
        geomType = layer.geometryType()
        if not geomType in (QgsWkbTypes.PointGeometry, QgsWkbTypes.LineGeometry, QgsWkbTypes.PolygonGeometry):
            self.close()
            return
        if geomType == QgsWkbTypes.PointGeometry:
            self.pointRubberGroup.hide()

        # editors management
        self.editorLayout = QGridLayout(self.editorContainer)
        self.editor = GeomEditor(layer, feature.geometry())
        self.displayCombo.setCurrentIndex(0)
        self.displayCombo.currentIndexChanged.connect(self.setEditor)
        self.setEditor()

        # rubber bands
        self.featureRubber = QgsRubberBand(mapCanvas)
        self.currentPointRubber = QgsRubberBand(mapCanvas)
        self.settings.setting("featureRubberColor").valueChanged.connect(self.updateFeatureRubber)
        self.settings.setting("featureRubberSize").valueChanged.connect(self.updateFeatureRubber)
        self.settings.setting("currentPointRubberSize").valueChanged.connect(self.updateCurrentPointRubber)
        self.settings.setting("currentPointRubberColor").valueChanged.connect(self.updateCurrentPointRubber)
        self.settings.setting("currentPointRubberIcon").valueChanged.connect(self.updateCurrentPointRubber)
        self.updateFeatureRubber()
        self.updateCurrentPointRubber()
        self.geometryChanged()

        # GUI signals connection
        self.applyButton.clicked.connect(self.applyGeometry)
        self.resetButton.clicked.connect(self.resetGeometry)
        self.sketchGeometry.clicked.connect(self.geometryChanged)
        self.displayPointRubber.clicked.connect(self.currentPointRubber.reset)
        self.layerEditable()
        layer.editingStopped.connect(self.layerEditable)
        layer.editingStarted.connect(self.layerEditable)

        # set texts in UI
        self.layerLabel.setText(layer.name())
        try:
            featureTitle = str(feature[layer.displayField()])
        except KeyError:
            featureTitle = ""
        if featureTitle == "":
            featureTitle = str(feature.id())
        self.featureEdit.setText(featureTitle)

    def setEditor(self):
        self.editorLayout.removeWidget(self.editor)
        geom = self.editor.getGeom()
        idx = self.displayCombo.currentIndex()
        if idx == -99999:
            editor = CellEditor
        elif idx == 0:
            editor = WktEditor
        elif idx == 1:
            editor = WkbEditor
        else:
            self.editor = GeomEditor
            return
        self.editor = editor(self.layer, geom, self)
        self.editorLayout.addWidget(self.editor, 0, 0, 1, 1)

        self.editor.currentPointChanged.connect(self.drawCurrentPoint)
        self.editor.geometryChanged.connect(self.geometryChanged)

    def resetGeometry(self):
        self.editor.setGeom(self.initialGeometry)

    def closeEvent(self, e):
        self.featureRubber.reset()
        self.currentPointRubber.reset()
        self.layer.editingStarted.disconnect(self.layerEditable)
        self.layer.editingStopped.disconnect(self.layerEditable)
        self.editor.closeEditor()
        QDialog.closeEvent(self, e)

    def layerEditable(self):
        layerIsEditable = self.layer.isEditable()
        self.resetButton.setEnabled(layerIsEditable)
        self.applyButton.setEnabled(layerIsEditable)

    def geometryChanged(self):
        self.featureRubber.reset()
        self.currentPointRubber.reset()
        if self.editor.isGeomValid():
            self.displayCombo.setEnabled(True)
            self.applyButton.setEnabled(self.layer.isEditable())
            geomStatus = "Geometry is valid"
            if self.sketchGeometry.isChecked():
                self.featureRubber.setToGeometry(self.editor.getGeom(), self.layer)
        else:
            self.applyButton.setEnabled(False)
            self.displayCombo.setEnabled(False)
            geomStatus = "Geometry is not valid"
        self.geomStatusLabel.setText(geomStatus)

    @pyqtSlot(QgsGeometry)
    def drawCurrentPoint(self, point):
        if self.displayPointRubber.isChecked():
            self.currentPointRubber.setToGeometry(point, None)
            self.mapCanvas.refresh()

    def applyGeometry(self):
        geometry = self.editor.getGeom()
        if geometry is not None:
            self.layer.changeGeometry(self.feature.id(), geometry)
            self.layer.updateExtents()
            try:
                self.layer.setCacheImage(None)
            except:
                pass
            self.layer.triggerRepaint()
            
    def updateFeatureRubber(self):
        self.featureRubber.setColor(self.settings.value("featureRubberColor"))
        self.featureRubber.setWidth(int(self.settings.value("featureRubberSize")))
        self.layer.triggerRepaint()
        
    def updateCurrentPointRubber(self):
        self.currentPointRubber.setIconSize(self.settings.value("currentPointRubberSize"))
        self.currentPointRubber.setColor(self.settings.value("currentPointRubberColor"))
        self.currentPointRubber.setIcon(self.settings.value("currentPointRubberIcon"))
        self.mapCanvas.refresh()
