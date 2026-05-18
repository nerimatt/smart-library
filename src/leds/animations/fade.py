from random import randint

from ..LED_cluster import LED_cluster

from .animation import Animation

class fade_animation(Animation):
    _animation_speed = 150

    def __init__(self, cluster: LED_cluster, default_color = (255, 255, 255), random_colors = False):
        super().__init__("fade", cluster)

        self.set_options({
            "color": default_color,
            "random_colors": random_colors
        })

        # save loop in var so it doesnt restart each time (first iter is fired automatically,
        # but it starts from 0 so we dont notice)
        self._steps = self._step_loop()

    # TODO: make better to avoid colors like black or greylike (maybe use some hsl formulas)
    def get_random_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def _create_range(self):
        l = [ x / 100.0 for x in range(0, 10000 + self._animation_speed, self._animation_speed)]
        return l + l[::-1]

    # prepare infinite frames (it is an iterable)
    def _step_loop(self):
        while True:
            for i in self._create_range(): # [0...98,99,100,99...0]
                self.cluster.fill(tuple( int( x * i / 100 ) for x in self.options["color"] ))
                yield 0 # retain loop and do one step every time

            if self.options["random_colors"]:
                self.options["color"] = self.get_random_color()

