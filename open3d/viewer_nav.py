__all__ = ['ViewerNav']

import json
import numpy as np
import open3d as o3d
import os

class ViewerNav:
    def __init__(self, config='config.json'):
        self.vis = None
        self.first_update = True
        self.stop_update = False
        self.current_frame = 0
        self.mesh = None
        self.length = 0

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
        self.vis.register_key_callback(ord(','), self.callback_prev_frame)
        self.vis.register_key_callback(ord('.'), self.callback_next_frame)

    def disconnect(self):
        if self.vis is not None:
            self.vis.destroy_window()
            self.vis.close()
        self.vis = None
        self.first_update = True

    def load_mesh(self, directory, length=None):
        if length is None:
            self.length = len(os.listdir(directory))
        else:
            self.length = int(length)
        self.mesh_dir = directory

    def get_mesh(self, i):
        mesh = o3d.io.read_triangle_mesh(os.path.join(self.mesh_dir, f'{i:04d}.obj'))
        return mesh
        
    def _mesh_preprocess(self, mesh):
        # add lines for each mesh's preprocessing here
        mesh.compute_vertex_normals()
        return mesh

    def update(self, i):
        self.vis.clear_geometries()
        current_mesh = self._mesh_preprocess(self.get_mesh(i))
        self.vis.add_geometry(current_mesh)
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

    def callback_prev_frame(self, vis):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.update(self.current_frame)
        return False

    def callback_next_frame(self, vis):
        if self.current_frame < self.length - 1:
            self.current_frame += 1
            self.update(self.current_frame)
        return False


if __name__ == '__main__':
    with ViewerNav() as viewer:
        viewer.load_mesh('object')
        viewer.update(0)
        viewer.pause()