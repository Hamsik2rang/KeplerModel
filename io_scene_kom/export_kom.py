import math
from math import radians
import mathutils
import bpy

# 1. Polygon이 4개 vertex로 이루어지므로 3-3으로 쪼개야 함
# 2. 오른손 좌표계를 사용하므로 왼손 좌표계로 변경해야 함
# 3. 맵 툴이 아니므로 오브젝트의 위치나 회전 상태 등은 저장하지 않음


def WriteVertices(f, mesh):
    mesh_polygons = mesh.polygons[:]
    mesh_vertices = mesh.vertices[:]
    # write vertex count
    vertex_count = 0
    for polygon in mesh_polygons:
        for vertex in polygon.vertices:
            vertex_count += 1

    f.write("# " + str(vertex_count) + " vertices\n")
    # write vertex data
    for polygon in mesh.polygons:
        for i in range(len(polygon.vertices)):
            v = mesh_vertices[polygon.vertices[i]]
            f.write(
                "v "
                + " "
                + str("%.6f" % v.co[0])
                + " "
                + str("%.6f" % v.co[1])
                + " "
                + str("%.6f" % v.co[2])
                + "\n"
            )


def WriteUVs(f, mesh):
    if len(mesh.uv_layers) == 0:
        return

    mesh_polygons = mesh.polygons[:]
    mesh_uvs = mesh.uv_layers.active.data[:]
    # write uv count
    uv_count = len(mesh_uvs)
    f.write("# " + str(uv_count) + " uvs\n")
    # write uv data
    for polygon in mesh_polygons:
        for i in range(len(polygon.vertices)):
            uv = mesh_uvs[polygon.vertices[i]]
            # reverse uv to convert from right-handed to left-handed(1.0 - uv[1])
            f.write(
                "vt"
                + " "
                + str("%.6f" % uv.uv[0])
                + " "
                + str("%.6f" % (1.0 - uv.uv[1]))
                + "\n"
            )


def WriteVertexNormals(f, mesh):
    mesh_polygons = mesh.polygons[:]
    mesh_vertices = mesh.vertices[:]

    # count vertex count (same with normal count)
    normal_count = 0
    for polygon in mesh_polygons:
        for vertex in polygon.vertices:
            normal_count += 1

    f.write("# " + str(normal_count) + " normals\n")
    # write normal data
    for polygon in mesh_polygons:
        for vertex in polygon.vertices:
            if mesh.use_auto_smooth == False:
                normal = polygon.normal
            else:
                normal = mesh.vertices[vertex].normal

            f.write(
                "vn"
                + " "
                + str("%.6f" % normal.x)
                + " "
                + str("%.6f" % normal.y)
                + " "
                + str("%.6f" % normal.z)
                + "\n"
            )


def WritePolygonIndices(f, mesh):
    mesh_uvs = mesh.uv_layers.active.data
    f.write("# " + str(len(mesh.polygons[:]) * 2) + " tris\n")
    for polygon in mesh.polygons:
        indices = []
        for index in polygon.loop_indices:
            indices.append(index)
        # convert from right-handed to left-handed
        # 3 2 1
        if len(indices) == 4:
            f.write(
                "f"
                + " "
                + str(indices[3])
                + "/"
                + str(indices[2])
                + "/"
                + str(indices[1])
                + "\n"
            )
            # 3 1 0
            f.write(
                "f "
                + " "
                + str(indices[3])
                + "/"
                + str(indices[1])
                + "/"
                + str(indices[0])
                + "\n"
            )
        elif len(indices) == 3:
            f.write(
                "f"
                + " "
                + str(indices[0])
                + " "
                + str(indices[2])
                + " "
                + str(indices[1])
                + "\n"
            )


def ExportFile(filepath):
    bpy.ops.object.mode_set(mode="OBJECT")

    print("Exporting File: " + filepath)
    f = open(filepath, "w", encoding="utf8", newline="\n")

    for object in bpy.data.objects:
        # eliminate unnecessary objects
        if object.name == "Camera" or object.name == "Light":
            continue

        f.write("# " + object.name + "\n")
        mesh = object.data

        WriteVertices(f, mesh)
        WriteUVs(f, mesh)
        WriteVertexNormals(f, mesh)
        WritePolygonIndices(f, mesh)
        f.write("\n")
    f.close()

    return {"FINISHED"}
