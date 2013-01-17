"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module

"""
def name():
    return "Plain Geometry Editor"
def description():
    return "Edit geometry of features using WKT"
def version():
    return "Version 1.0"
def icon():
    return "icons/plaingeometryeditor-32.png"
def qgisMinimumVersion():
    return "1.8"
def classFactory(iface):
    from plaingeometryeditor import PlainGeometryEditor
    return PlainGeometryEditor(iface)
