"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Apr. 2013
"""
from PyQt4.QtGui import QColor,QDialog

from qgis.gui import QgsRubberBand

from qgistools.pluginsettings import *

pluginName = "plaingeometryeditor"

mySettings = [
	Bool(   pluginName, "sketchGeometry"    , "global",  True ),
	Color(  pluginName, "featureRubberColor"       , "global",  QColor(0,0,255) ),
	Double( pluginName, "featureRubberSize"        , "global",  .6 ),
	Integer(pluginName, "featureRubberAlpha"       , "global",  100 ),
	Color(  pluginName, "currentPointRubberColor"        , "global",  QColor(255,0,0) ),
	Integer(pluginName, "currentPointRubberIcon"        , "global",  int(QgsRubberBand.ICON_BOX) ),
	Integer(pluginName, "currentPointRubberSize"         , "global",  3 ),
	Bool(   pluginName, "displayPointRubber", "global",  True )
]
