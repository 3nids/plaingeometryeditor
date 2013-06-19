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

from PyQt4.QtCore import Qt, pyqtSlot
from PyQt4.QtGui import QGridLayout, QDialog
from qgis.core import QGis, QgsGeometry
from qgis.gui import QgsRubberBand

from ..qgissettingmanager import SettingDialog
from ..core.mysettings import MySettings
from ..geomeditors import GeomEditor, CellEditor, WkbEditor, WktEditor
from ..ui.ui_geomeditor import Ui_GeomEditor


class GeomEditorDialog(QDialog, Ui_GeomEditor, SettingDialog):
    def __init__(self, layer, feature, mapCanvas, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings, False, True)
        self.mapCanvas = mapCanvas

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.editor = GeomEditor(layer, feature)
        self.feature = feature
        self.layer = layer

        geomType = layer.geometryType()
        if not geomType in (QGis.Point, QGis.Line, QGis.Polygon):
            self.close()
            return
        if geomType == QGis.Point:
            self.pointRubberGroup.hide()

        self.featureRubber = QgsRubberBand(mapCanvas)
        self.currentPointRubber = QgsRubberBand(mapCanvas)
        self.settings.setting("featureRubberColor").valueChanged.connect(self.updateFeatureRubber)
        self.settings.setting("featureRubberSize").valueChanged.connect(self.updateFeatureRubber)
        self.settings.setting("currentPointRubberSize").valueChanged.connect(self.updateCurrentPointRubber)
        self.settings.setting("currentPointRubberColor").valueChanged.connect(self.updateCurrentPointRubber)
        self.settings.setting("currentPointRubberIcon").valueChanged.connect(self.updateCurrentPointRubber)
        self.updateFeatureRubber()
        self.updateCurrentPointRubber()

        self.displayCombo.currentIndexChanged.connect(self.setEditor)
        self.displayCombo.setCurrentIndex(1)

        # GUI stuff
        self.finished.connect(self.finish)
        self.applyButton.clicked.connect(self.applyGeometry)
        self.resetButton.clicked.connect(self.editor.resetGeom)

        self.sketchGeometry.clicked.connect(self.geometryChanged)


        self.layerEditable()
        layer.editingStopped.connect(self.layerEditable)
        layer.editingStarted.connect(self.layerEditable)

        self.layerLabel.setText(layer.name())
        featureTitle = "%s" % feature[layer.displayField()]
        if featureTitle == "":
            featureTitle = "%s" % feature.id()
        self.featureEdit.setText(featureTitle)

    def setEditor(self):
        idx = self.displayCombo.currentIndex()
        if idx == 0:
            editor = CellEditor
        elif idx == 1:
            editor = WktEditor
        elif idx == 2:
            editor = WkbEditor
        else:
            self.editor = GeomEditor
            return
        self.editorLayout = QGridLayout(self.editorContainer)
        self.editor = editor(self.layer, self.feature)
        self.editorLayout.addWidget(self.editor, 0, 0, 1, 1)

        self.editor.currentPointChanged.connect(self.drawCurrentPoint)
        self.editor.geometryChanged.connect(self.geometryChanged)

    def finish(self, state):
        self.featureRubber.reset()
        self.currentPointRubber.reset()
        self.layer.editingStarted.disconnect(self.layerEditable)
        self.layer.editingStopped.disconnect(self.layerEditable)
        #self.close()

    def layerEditable(self):
        layerIsEditable = self.layer.isEditable()
        self.resetButton.setEnabled(layerIsEditable)
        self.applyButton.setEnabled(layerIsEditable)

    def geometryChanged(self):
        self.featureRubber.reset()
        if self.editor.isGeomValid():
            self.displayCombo.setEnabled(True)
            self.applyButton.setEnabled(self.layer.isEditable())
            geomStatus = "Geometry is valid"
            if self.sketchGeometry.isChecked():
                self.featureRubber.setToGeometry(self.editor.getGeom, self.layer)
        else:
            self.applyButton.setEnabled(False)
            self.displayCombo.setEnabled(False)
            geomStatus = "Geometry is not valid"
        self.geomStatusLabel.setText(geomStatus)

    @pyqtSlot(QgsGeometry)
    def drawCurrentPoint(self, point):
        self.currentPointRubber.setToGeometry(point, None)
        self.mapCanvas.refresh()

    def applyGeometry(self):
        geometry = self.editor.getGeom()
        if geometry is not None:
            self.layer.changeGeometry(self.feature.id(), geometry)
            self.layer.triggerRepaint()
            self.close()
            
    def updateFeatureRubber(self):
        self.featureRubber.setColor(self.settings.value("featureRubberColor"))
        self.featureRubber.setWidth(self.settings.value("featureRubberSize"))
        self.layer.triggerRepaint()
        
    def updateCurrentPointRubber(self):
        self.currentPointRubber.setIconSize(self.settings.value("currentPointRubberSize"))
        self.currentPointRubber.setColor(self.settings.value("currentPointRubberColor"))
        self.currentPointRubber.setIcon(self.settings.value("currentPointRubberIcon"))
        self.mapCanvas.refresh()
