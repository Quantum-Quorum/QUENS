import sys

import numpy as np

from vispy import app, scene
from vispy.color import Color


class SpaceMapDashboard:
    def __init__(self):
        self.canvas = scene.SceneCanvas(keys='interactive', title='QUENS - Level 2: ODIN Dashboard', show=True,
                                        size=(1024, 768))
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.view.camera.scale_factor = 20.0
        self.view.bgcolor = 'black'
        self.stars = scene.visuals.Markers(parent=self.view.scene)
        star_pos = (np.random.rand(1000, 3) - 0.5) * 100
        self.stars.set_data(star_pos, face_color=(1, 1, 1, 0.5), size=2, symbol='o')
        self.axis = scene.visuals.XYZAxis(parent=self.view.scene)
        self.spacecraft = scene.visuals.Markers(parent=self.view.scene)
        self.spacecraft.set_data(
            np.array([[0.0, 0.0, 0.0]]),
            edge_color='white',
            face_color='green',
            size=15,
            symbol='diamond'
        )

        self.pulsars = scene.visuals.Markers(parent=self.view.scene)
        self.pulsar_positions = np.array([
            [5.0, 5.0, 2.0],
            [-8.0, 6.0, -3.0],
            [2.0, -7.0, 8.0]
        ])

        self.pulsars.set_data(
            self.pulsar_positions,
            edge_color='cyan',
            face_color='blue',
            size=12,
            symbol='o'
        )

        self.text = scene.visuals.Text(text='PSR J0030+0451', parent=self.view.scene, color='white',
                                       pos=[5.0, 5.5, 2.0], font_size=10)

        self.lines = scene.visuals.Line(parent=self.view.scene, color='green', method='gl')

        # Setup animation timer
        self.timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.time = 0.0

    def on_timer(self, event):
        self.time += 0.02

        sc_pos = np.array([[np.sin(self.time) * 3, np.cos(self.time) * 3, np.sin(self.time * 0.5)]])
        self.spacecraft.set_data(
            sc_pos,
            edge_color='white',
            face_color='green',
            size=15,
            symbol='diamond'
        )

        line_coords = []
        for p in self.pulsar_positions:
            line_coords.append(sc_pos[0])
            line_coords.append(p)

        self.lines.set_data(pos=np.array(line_coords))


if __name__ == '__main__':

    dash = SpaceMapDashboard()
    if sys.flags.interactive != 1:
        app.run()
