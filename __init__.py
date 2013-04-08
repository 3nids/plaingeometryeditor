"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Plain Geometry Editor
QGIS module

"""
def classFactory(iface):
    from plaingeometryeditor import PlainGeometryEditor
    return PlainGeometryEditor(iface)
