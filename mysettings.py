"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Apr. 2013
"""
from PyQt4.QtGui import QColor,QDialog

from qgistools.pluginsettings import *

pluginName = "plaingeometryeditor"

mySettings = [
	# global settings
	Bool(   pluginName, "sketchGeometry", "global",  True ),
	Color(  pluginName, "rubberColor"   , "global",  QColor(0,0,255) )
]
