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

from qgissettingmanager import SettingDialog

from ui.ui_geomeditor import Ui_GeomEditor

from geomeditors.celleditor import CellEditor
from geomeditors.wkteditor import WktEditor
from geomeditors.wkbeditor import WkbEditor

from core.mysettings import MySettings


class GeomEditorDialog(QDialog, Ui_GeomEditor, SettingDialog):
    def __init__(self, iface, layer, feature):
        self.iface = iface
        QDialog.__init__(self, iface.mainWindow())
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings, False, True)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.feature = feature
        self.layer = layer
        self.initialGeom = QgsGeometry(feature.geometry())
        self.modifiedGeom = QgsGeometry(feature.geometry())
        self.geomType = self.initialGeom.type()
        self.cellEditor = CellEditor(self)
        self.wktEditor = WktEditor(self)
        self.wkbEditor = WkbEditor(self)
        if not self.geomType in (QGis.Point, QGis.Line, QGis.Polygon):
            self.close()
            return
        if self.geomType == QGis.Point:
            self.pointRubberGroup.hide()

        self.featureRubber = QgsRubberBand(iface.mapCanvas())
        self.currentPointRubber = QgsRubberBand(iface.mapCanvas())
        self.settings.setting("featureRubberColor").valueChanged.connect(self.updateFeatureRubber)
        self.settings.setting("featureRubberSize").valueChanged.connect(self.updateFeatureRubber)
        self.settings.setting("currentPointRubberSize").valueChanged.connect(self.updateCurrentPointRubber)
        self.settings.setting("currentPointRubberColor").valueChanged.connect(self.updateCurrentPointRubber)
        self.settings.setting("currentPointRubberIcon").valueChanged.connect(self.updateCurrentPointRubber)
        self.updateFeatureRubber(None)
        self.updateCurrentPointRubber(None)

        self.displayCombo.setCurrentIndex(1)

        # GUI stuff
        QObject.connect(self , SIGNAL("finished(int)") , self.finish)
        QObject.connect(self.applyButton,    SIGNAL("clicked()"), self.applyGeometry)
        QObject.connect(self.sketchGeometry, SIGNAL("clicked()"), self.geomChanged)
        QObject.connect(self.geomTextEdit,   SIGNAL("textChanged()"), self.geomChanged)
        QObject.connect(self.geomTextEdit,   SIGNAL("cursorPositionChanged()"), self.getEditor().cursorPositionChanged)
        self.layerEditable()
        QObject.connect(layer, SIGNAL("editingStopped() "), self.layerEditable)
        QObject.connect(layer, SIGNAL("editingStarted() "), self.layerEditable)
        self.layerLabel.setText(layer.name())
        featureTitle = "%s" % feature[layer.displayField()]
        if featureTitle == "":
            featureTitle = "%s" % feature.id()
        self.featureEdit.setText(featureTitle)

        # write geometry in text edit
        self.getEditor().setGeom(self.initialGeom)

    def getEditor(self):
        idx = self.displayCombo.currentIndex()
        if idx == 0:
            return self.cellEditor
        elif idx == 1:
            return self.wktEditor
        elif idx == 2:
            return self.wkbEditor
        else:
            return None

    @pyqtSignature("on_displayCombo_currentIndexChanged(int)")
    def on_displayCombo_currentIndexChanged(self, idx):
        self.getEditor().setGeom(self.modifiedGeom)

    def finish(self, state):
        self.featureRubber.reset()
        self.currentPointRubber.reset()
        QObject.disconnect(self.layer, SIGNAL("editingStarted()"), self.layerEditable)
        QObject.disconnect(self.layer, SIGNAL("editingStopped()"), self.layerEditable)
        self.close()

    @pyqtSignature("on_resetButton_clicked()")
    def on_resetButton_clicked(self):
        self.getEditor().setGeom(self.initialGeom)

    @pyqtSignature("on_copyButton_clicked()")
    def on_copyButton_clicked(self):
        QApplication.clipboard().setText(self.geomTextEdit.toPlainText())

    def layerEditable(self):
        layerIsEditable = self.layer.isEditable()
        self.geomTextEdit.setEnabled(layerIsEditable)
        self.resetButton.setEnabled(layerIsEditable)
        self.applyButton.setEnabled(layerIsEditable)

    def geomChanged(self):
        self.featureRubber.reset()
        editor = self.getEditor()
        if editor.isGeomValid():
            bgColor = "white"
            self.modifiedGeom = editor.getGeom()
            self.displayCombo.setEnabled(True)
            self.applyButton.setEnabled(self.layer.isEditable())
            geomStatus = "Geometry is valid"
            if self.sketchGeometry.isChecked():
                self.featureRubber.setToGeometry(self.modifiedGeom, self.layer)
        else:
            bgColor = "red"
            self.applyButton.setEnabled(False)
            self.displayCombo.setEnabled(False)
            geomStatus = "invalid"

        p = self.geomTextEdit.palette()
        p.setColor(QPalette.Base, QColor(bgColor))
        self.geomTextEdit.setPalette(p)
        self.geomStatusLabel.setText(geomStatus)

    def currentPointChanged(self, point):
        self.currentPointRubber.setToGeometry(point , self.layer)

    def applyGeometry(self):
        geometry = self.getEditor().getGeom()
        if geometry:
            self.layer.changeGeometry(self.feature.id(), geometry)
            self.iface.mapCanvas().refresh()
            self.close()
            
    def updateFeatureRubber(self, i):
        self.featureRubber.setColor(self.settings.value("featureRubberColor"))
        self.featureRubber.setWidth(self.settings.value("featureRubberSize"))
        self.iface.mapCanvas().refresh()
        
    def updateCurrentPointRubber(self, i):
        self.currentPointRubber.setIconSize(self.settings.value("currentPointRubberSize"))
        self.currentPointRubber.setColor(self.settings.value("currentPointRubberColor"))
        self.currentPointRubber.setIcon(self.settings.value("currentPointRubberIcon"))
        self.iface.mapCanvas().refresh()
