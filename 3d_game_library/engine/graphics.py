from panda3d.core import GeomNode, Geom, GeomVertexFormat, GeomVertexData
from panda3d.core import GeomTriangles, GeomVertexWriter, NodePath
from OpenGL.GL import *

def create_custom_node():
    # Create a basic geometry using Panda3D
    format = GeomVertexFormat.get_v3()
    vdata = GeomVertexData('vertices', format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')

    vertex.add_data3f(0, 0, 0)
    vertex.add_data3f(1, 0, 0)
    vertex.add_data3f(1, 1, 0)
    vertex.add_data3f(0, 1, 0)

    triangles = GeomTriangles(Geom.UHStatic)
    triangles.add_vertices(0, 1, 2)
    triangles.add_vertices(2, 3, 0)

    geom = Geom(vdata)
    geom.add_primitive(triangles)

    node = GeomNode('custom_node')
    node.add_geom(geom)

    return NodePath(node)
