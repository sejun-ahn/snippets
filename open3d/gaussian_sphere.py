# drawing a gaussian sphere
__all__ = ['create_gaussian_sphere', 'create_x_plane', 'create_y_plane', 'create_z_plane', 'image_projection']

import open3d as o3d
import numpy as np

def create_gaussian_sphere(resolution=20):
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=1.0, resolution=resolution)
    r"""
    Create a gaussian sphere.
    Parameters
    ----------
    resolution : int, default = 20
        Resolution of the sphere.
    Returns
    -------
    open3d.geometry.TriangleMesh
        A gaussian sphere.
    """
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

def create_x_plane(thickness=0.01):
    r"""
    Create a torus representing the x-plane.
    Parameters
    ----------
    thickness : float, default = 0.01
        Thickness of the torus.
    Returns
    -------
    open3d.geometry.TriangleMesh
        A torus representing the x-plane.
    """
    x = o3d.geometry.TriangleMesh.create_torus(1.0, thickness)
    x.paint_uniform_color([1, 0, 0])
    x.rotate(x.get_rotation_matrix_from_xyz((0, np.radians(90), 0)), center=(0, 0, 0))
    x.compute_vertex_normals()
    return x

def create_y_plane(thickness=0.01):
    r"""
    Create a torus representing the y-plane.
    Parameters
    ----------
    thickness : float, default = 0.01
        Thickness of the torus.
    Returns
    -------
    open3d.geometry.TriangleMesh
        A torus representing the y-plane.
    """
    y = o3d.geometry.TriangleMesh.create_torus(1.0, thickness)
    y.paint_uniform_color([0, 1, 0])
    y.rotate(y.get_rotation_matrix_from_xyz((np.radians(90), 0, 0)), center=(0, 0, 0))
    y.compute_vertex_normals()
    return y

def create_z_plane(thickness=0.01):
    r"""
    Create a torus representing the z-plane.
    Parameters
    ----------
    thickness : float, default = 0.01
        Thickness of the torus.
    Returns
    -------
    open3d.geometry.TriangleMesh
        A torus representing the z-plane.
    """
    z = o3d.geometry.TriangleMesh.create_torus(1.0, thickness)
    z.paint_uniform_color([0, 0, 1])
    z.compute_vertex_normals()
    return z

def image_projection(image, fov_horizontal=60.0):
    r"""
    Project an image onto a sphere.
    Parameters
    ----------
    image : numpy.ndarray
        The image to be projected. The image should be in RGB format.
    fov_horizontal : float, default = 60.0
        Horizontal field of view in degrees.
    Returns
    -------
    open3d.geometry.PointCloud
        A point cloud representing the image pixels projected onto a sphere.
    """
    h,w,c = image.shape
    fov_vertical = fov_horizontal * h / w
    h_angles = np.linspace(-fov_horizontal/2, fov_horizontal/2, w)
    v_angles = np.linspace(-fov_vertical/2, fov_vertical/2, h)
    h_grid, v_grid = np.meshgrid(h_angles, v_angles)
    h_grid = np.radians(h_grid)
    v_grid = np.radians(v_grid)
    x = np.cos(v_grid) * np.cos(h_grid)
    y = np.cos(v_grid) * np.sin(h_grid)
    z = np.sin(v_grid)
    points = np.stack([x,y,z], axis=-1).reshape(-1,3)
    colors = image.reshape(-1,3)/255.0
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd

