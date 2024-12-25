# drawing a gaussian sphere
__all__ = ['create_gaussian_sphere']

import open3d as o3d
import numpy as np

def create_gaussian_sphere(resolution=20):
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=1.0, resolution=resolution)
    # https://www.open3d.org/docs/release/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.create_sphere
    # Being split by resolution,
    # a gaussian sphere will have
    # resolution + 1 horizontal lines and
    # 2 * resolution vertical lines

    lineset = o3d.geometry.LineSet()
    lineset.points = sphere.vertices

    res_2 = resolution * 2

    hlines = []
    for j in range(resolution-1):
        hlines.append([1+(j+1)*res_2, 2+j*res_2])
        for i in range(2+j*res_2, 1+(j+1)*res_2):
            hlines.append([i, i+1])
        
    vlines = []
    for j in range(resolution*2):
        vlines.append([0, 2+j])
        vlines.append([res_2*(resolution-2)+2+j, 1])
        for i in range(resolution-2):
            vlines.append([2+i*res_2+j, 2+(i+1)*res_2+j])

    lines = hlines + vlines
    lineset.lines = o3d.utility.Vector2iVector(lines)
    
    lines_color = [[0.4, 0.4, 0.4] for i in range(len(lines))]
    lineset.colors = o3d.utility.Vector3dVector(lines_color)

    lineset.rotate(lineset.get_rotation_matrix_from_xyz((np.radians(90), 0, 0)), center=(0, 0, 0))
    
    return lineset