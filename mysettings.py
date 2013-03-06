"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2013
"""
from pluginsettings import PluginSettings

from PyQt4.QtGui import QColor

class MySettings(PluginSettings):
	def __init__(self,uiObject=None):
		PluginSettings.__init__(self, "plaingeometryeditor",uiObject)
		self.addSetting("rubberColor", "global", "color", QColor(0,0,255),True)
		self.addSetting("sketchGeometry", "global", "bool", True, True)
		

