__all__ = ['ViewerNavRotate']

import json
import numpy as np
import open3d as o3d
import os
from copy import deepcopy

class ViewerNavRotate:
    def __init__(self, config='config.json'):
        self.vis = None
        self.first_update = True
        self.stop_update = False
        self.current_angle = 0
        self.mesh = None
        

        with open(config, 'r') as f:
            cfg = json.load(f)
            self.height = cfg['height']
            self.width = cfg['width']
            self.window_name = cfg['window_name']
        
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.vis is not None:
            self.vis.destroy_window()
            self.vis.close()
        self.vis = None
        self.first_update = True

    def connect(self):
        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window(window_name=self.window_name, width=self.width, height=self.height, visible=True)
        self.vis.register_key_callback(ord('Q'), self.callback_quit)
        self.vis.register_key_callback(ord(','), self.callback_decrease_angle)
        self.vis.register_key_callback(ord('.'), self.callback_increase_angle)

    def disconnect(self):
        if self.vis is not None:
            self.vis.destroy_window()
            self.vis.close()
        self.vis = None
        self.first_update = True

    def load_mesh(self, obj_dir):
        self.mesh = o3d.io.read_triangle_mesh(obj_dir)
        self.mesh.compute_vertex_normals()

    def get_mesh(self):
        mesh = deepcopy(self.mesh)
        return mesh

    def update(self, i):
        self.vis.clear_geometries()
        mesh = self.get_mesh()
        mesh.rotate(mesh.get_rotation_matrix_from_xyz((0, np.radians(i), 0)), center=(0, 0, 0))
        self.vis.add_geometry(mesh)
        print(i)

        self.vis.poll_events()
        self.vis.update_renderer()
        self.first_update = False

    def pause(self):
        self.stop_update = False
        while not self.stop_update:
            self.vis.poll_events()
            self.vis.update_renderer()

    def callback_quit(self, vis):
        self.stop_update = True
        return False

    def callback_decrease_angle(self, vis):
        self.current_angle -= 1
        self.current_angle %= 360
        self.update(self.current_angle)
        return False

    def callback_increase_angle(self, vis):
        self.current_angle += 1
        self.current_angle %= 360
        self.update(self.current_angle)
        return False


if __name__ == '__main__':
    with ViewerNavRotate() as viewer:
        viewer.load_mesh('./object/0000.obj')
        viewer.update(0)
        viewer.pause()