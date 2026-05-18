# equal to fade but all colors randomly throuout of strip

# check hue rotations

from ..LED_cluster import LED_cluster
from .animation import Animation

from ..color import RGBRotate

class rainbow_animation(Animation):
    def __init__(self, cluster: LED_cluster):
        super().__init__("rainbow", cluster)

        self._steps = self._step_loop()

        self.hue_rotation = RGBRotate()
        self.hue_rotation.set_hue_rotation(100)


    def _step_loop(self):
        col = (192, 255, 100)
        while True:
            col = self.hue_rotation.apply(*col)
            self.cluster.fill(col)

            yield 0

