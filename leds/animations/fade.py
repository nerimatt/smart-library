from leds.LED_cluster import LED_cluster

from leds.animations.animation import Animation

class fade_animation(Animation):

    def __init__(self, cluster: LED_cluster, default_color = (255, 255, 255)):
        self.cluster = cluster

        self.set_options({"color": default_color})
        self._steps = self._step_loop() # save loop in var so it doesnt restart each time


    # prepare infinite frames (it is an iterable)
    def _step_loop(self):
        while True:
            for i in list(range(0, 100, self._animation_speed)) + list(range(100, -1, -self._animation_speed)): # [0...98,99,100,99...0]
                self.cluster.fill(tuple( int( x * i / 100 ) for x in self.options["color"] ))
                yield 0 # retain loop and do one step every time



    def step(self):
        return next(self._steps)

