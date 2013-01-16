# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geomeditor.ui'
#
# Created: Wed Jan 16 15:42:13 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GeomEditor(object):
    def setupUi(self, GeomEditor):
        GeomEditor.setObjectName(_fromUtf8("GeomEditor"))
        GeomEditor.resize(451, 367)
        self.gridLayout = QtGui.QGridLayout(GeomEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sketchBox = QtGui.QCheckBox(GeomEditor)
        self.sketchBox.setChecked(True)
        self.sketchBox.setObjectName(_fromUtf8("sketchBox"))
        self.gridLayout.addWidget(self.sketchBox, 0, 0, 1, 1)
        self.resetButton = QtGui.QPushButton(GeomEditor)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.gridLayout.addWidget(self.resetButton, 2, 1, 1, 1)
        self.applyButton = QtGui.QPushButton(GeomEditor)
        self.applyButton.setObjectName(_fromUtf8("applyButton"))
        self.gridLayout.addWidget(self.applyButton, 2, 2, 1, 1)
        self.wktText = QtGui.QTextEdit(GeomEditor)
        self.wktText.setObjectName(_fromUtf8("wktText"))
        self.gridLayout.addWidget(self.wktText, 1, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.validityStatusLabel = QtGui.QLabel(GeomEditor)
        self.validityStatusLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.validityStatusLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.validityStatusLabel.setObjectName(_fromUtf8("validityStatusLabel"))
        self.gridLayout.addWidget(self.validityStatusLabel, 0, 1, 1, 2)

        self.retranslateUi(GeomEditor)
        QtCore.QMetaObject.connectSlotsByName(GeomEditor)

    def retranslateUi(self, GeomEditor):
        GeomEditor.setWindowTitle(QtGui.QApplication.translate("GeomEditor", "Plain Geometry Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.sketchBox.setText(QtGui.QApplication.translate("GeomEditor", "Sketch on map", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("GeomEditor", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("GeomEditor", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.validityStatusLabel.setText(QtGui.QApplication.translate("GeomEditor", "valid", None, QtGui.QApplication.UnicodeUTF8))

