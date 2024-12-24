__all__ = ['Viewer']


import numpy as np
import open3d as o3d

class Viewer:
    def __init__(self):
        self.vis = None
        self.first_update = True

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.vis is not None:
            self.vis.destroy_window()
            self.vis.close()
        self.vis = None
        self.first_update = True

    def update(self):
        self.vis.clear_geometries()

        # add lines (about the object to update) here

        self.vis.poll_events()
        self.vis.update_renderer()
        self.first_update = False

    def pause(self):
        while self.vis.poll_events():
            pass

if __name__ == '__main__':
    with Viewer() as viewer:
        viewer.update()
        viewer.pause()
