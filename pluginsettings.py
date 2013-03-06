"""
Custom settings for QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# possible types
valueTypes = ("string","double","integer","bool","color")

class PluginSettings(QObject):
	settingChanged = pyqtSignal(str)
	
	def __init__(self, pluginName, uiObject=None):
		QObject.__init__(self)
		self.settings = []
		self.pluginName = pluginName
		self.uiObject = uiObject

	def addSetting(self, name, scope, valueType, defaultValue, setValueOnWidgetUpdate=False):
		if self.__getSetting(name) is not None:
			raise NameError("%s already exist in settings." % name)
		if valueType not in valueTypes:
			raise NameError("Wrong type %s" % type)
		if scope not in ("global","project"):
			raise NameError("%s is not a valid scope. Must be project or global." % scope)
		SettingClass = globals()[ valueType+"PluginSetting" ]
		setting = SettingClass(self.pluginName, name, scope, defaultValue, self.uiObject, setValueOnWidgetUpdate)
		setting.valueChanged.connect(self.settingChanged)
		self.settings.append( setting )
		
	def __getSetting(self, name):
		for setting in self.settings:
			if setting.name == name:
				return setting
		return None

	def value(self, setting):
		setting = self.__getSetting(setting)
		if setting is None:
			raise NameError('%s has no setting %s' % (self.pluginName, setting) )
		return setting.getValue()

	def setValue(self, setting, value):
		setting = self.__getSetting(setting)
		if setting is None:
			raise NameError('%s has no setting %s' % (self.pluginName, setting) )
		self.__getSetting(setting).setValue(value)

	def setValuesFromWidgets(self):
		for setting in self.settings:
			if setting.widget is not None:
				setting.setValueFromWidget()



class PluginSetting(QObject):
	valueChanged = pyqtSignal(str)
	
	def __init__(self, pluginName, name, scope, defaultValue, uiObject=None, setValueOnWidgetUpdate=False):
		QObject.__init__(self)
		self.pluginName = pluginName
		self.name = name
		self.scope = scope
		self.defaultValue = [defaultValue.red(),defaultValue.green(),defaultValue.blue()]
		self.setValueOnWidgetUpdate = setValueOnWidgetUpdate
		self.widget = None
		if hasattr(uiObject,name):
			self.widget = getattr(uiObject,name)


class boolPluginSetting(PluginSetting):
	def __init__(self, pluginName, name, scope, defaultValue, uiObject=None, setValueOnWidgetUpdate=False):
		if scope not in ("global","project"):
			raise NameError("%s is not a valid scope. Must be project or global." % scope)
		PluginSetting.__init__(self, pluginName, name, scope, defaultValue, uiObject, setValueOnWidgetUpdate)
		self.check(defaultValue)
		self.currentValue = defaultValue
		self.__setUi()
		
	def check(self, boo):
		if type(boo)!=bool:
			raise NameError("Setting %s must be a boolean." % self.name)

	def setValue(self, boo):
		self.check(boo)
		if self.scope == "global":
			QSettings(self.pluginName,self.pluginName).setValue(self.name, boo )
		elif self.scope == "project":
			QgsProject.instance().writeEntryBool(pluginName, self.name, boo )

	def getValue(self):
		if self.scope == "global":
			return QSettings(self.pluginName,self.pluginName).value(self.name , self.defaultValue ).toBool()
		elif self.scope == "project":
			return QgsProject.instance().readBoolEntry(pluginName, self.name )
		
	def __setUi(self):
		if self.widget is None: return
		self.setChecked( self.getValue() )
		if self.setValueOnWidgetUpdate:
			QObject.connect(self.widget, SIGNAL("clicked()"), self.setValueFromWidget )

	def setValueFromWidget(self):
		self.setValue( self.widget.isChecked() )
		self.valueChanged.emit(self.name)
		
				
class colorPluginSetting(PluginSetting):	
	def __init__(self, pluginName, name, scope, defaultValue, uiObject=None, setValueOnWidgetUpdate=False):
		if scope not in ("global","project"):
			raise NameError("%s is not a valid scope. Must be project or global." % scope)
		PluginSetting.__init__(self, pluginName, name, scope, defaultValue, uiObject, setValueOnWidgetUpdate)
		self.check(defaultValue)
		self.currentValue = defaultValue
		self.__setUi()

	def check(self, color):
		if type(color)!=QColor:
			raise NameError("Color setting %s must be a QColor." % self.name)

	def setValue(self, color):
		self.check(color)
		if self.scope == "global":
			QSettings(self.pluginName,self.pluginName).setValue(self.name, [color.red(),color.green(),color.blue()] )
		elif self.scope == "project":
			QgsProject.instance().writeEntryBool(pluginName, self.name, QStringList(["%u"%color.red(),"%u"%color.green(),"%u"%color.blue()]) )

	def getValue(self):
		if self.scope == "global":
			color = QSettings(self.pluginName,self.pluginName).value(self.name , self.defaultValue ).toList()
		elif self.scope == "project":
			ok = bool()
			color = QgsProject.instance().readListEntry(pluginName, self.name, ok, self.defaultValue )
		if type(color)!=list or len(color)!=3:
			raise NameError("Color setting %s has been wrongly saved. It should be a list of 3 values (RGB)." % self.name)
		r = color[0].toInt()[0]
		g = color[1].toInt()[0]
		b = color[2].toInt()[0]
		return QColor(r,g,b)

	def __setUi(self):
		if self.widget is None: return
		self.setColorWidget( self.getValue() , False )
		QObject.connect(self.widget, SIGNAL("clicked()"), lambda: self.setColorWidget(QColorDialog.getColor(self.currentValue),True) )

	def setColorWidget(self, color, updateSetting):
		self.widget.setStyleSheet("background-color: rgb(%u,%u,%u)" % (color.red(),color.green(),color.blue()))
		self.currentValue = color
		if updateSetting and self.setValueOnWidgetUpdate:
			self.setValueFromWidget()

	def setValueFromWidget(self):
		self.setValue( self.currentValue )
		self.valueChanged.emit(self.name)
		




#	if scope == "global":
#		if type == "string":
#			self.set = lambda(v): QSettings(pluginName,pluginName).setValue(name, v)
#			self.get = lambda   : QSettings(pluginName,pluginName).value(   name , defaultValue ).toString()
#		elif type == "numeric":
#			self.set = lambda(v): QSettings(pluginName,pluginName).setValue(name, v)
#			self.get = lambda   : QSettings(pluginName,pluginName).value(   name , defaultValue ).toDouble()[0]
#
#	elif scope == "project":
#		if type == "string":
#			self.set = lambda(v): QgsProject.instance().writeEntry(pluginName, name, v)
#			self.get = lambda   : QgsProject.instance().readEntry( pluginName, name , defaultValue )
#		elif type == "numeric":
#			self.set = lambda(v): QgsProject.instance().writeEntryDouble(pluginName, name, v)
#			self.get = lambda   : QgsProject.instance().readDoubleEntry( pluginName, name , defaultValue )
#

