from pxr import Usd, UsdGeom

stage = Usd.Stage.Open('../rtx-remix/captures/meshes/mesh_0C62FD8A28F0F73C.usd')
stage.Export('mesh_0C62FD8A28F0F73C.usda')

xform_ref = stage.GetPrimAtPath("/mesh_0C62FD8A28F0F73C")


print( xform_ref )
