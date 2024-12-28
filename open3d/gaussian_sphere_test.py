from gaussian_sphere import *
import open3d as o3d
import numpy as np
import cv2

if __name__ == '__main__':
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='Gaussian Sphere', width=960, height=540, visible=True)
    
    vis.add_geometry(o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0))
    vis.add_geometry(create_gaussian_sphere())

    vis.add_geometry(create_x_plane())
    vis.add_geometry(create_y_plane())
    vis.add_geometry(create_z_plane())

    img = cv2.cvtColor(cv2.imread('milano.jpg'), cv2.COLOR_BGR2RGB)
    vis.add_geometry(image_projection(img, 120.0))

    vis.run()
    vis.destroy_window()