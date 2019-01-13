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

from qgis.PyQt.QtGui import QColor
from qgis.gui import QgsRubberBand

from ..qgissettingmanager import *

pluginName = "plaingeometryeditor"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        self.add_setting(Bool("sketchGeometry", Scope.Global,  True))
        self.add_setting(Color("featureRubberColor", Scope.Global,  QColor(0, 0, 255)))
        self.add_setting(Double("featureRubberSize", Scope.Global,  .6))
        self.add_setting(Integer("featureRubberAlpha", Scope.Global,  100))
        self.add_setting(Color("currentPointRubberColor", Scope.Global,  QColor(255, 0, 0)))
        self.add_setting(Integer("currentPointRubberIcon", Scope.Global,  int(QgsRubberBand.ICON_BOX)))
        self.add_setting(Integer("currentPointRubberSize", Scope.Global,  3))
        self.add_setting(Bool("displayPointRubber", Scope.Global,  True))
