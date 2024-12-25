from gaussian_sphere import create_gaussian_sphere
import open3d as o3d
import numpy as np

if __name__ == '__main__':
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='Gaussian Sphere', width=960, height=540, visible=True)
    
    vis.add_geometry(o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0))
    vis.add_geometry(create_gaussian_sphere())
    
    vis.run()
    vis.destroy_window()