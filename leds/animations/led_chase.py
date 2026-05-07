from leds.LED_cluster import LED_cluster

from leds.animations.animation import Animation

class led_chase_animation(Animation):

    def __init__(self, cluster: LED_cluster, snake_len = 3, bg_color = (0, 0, 0), snake_color = (255, 0, 0)):
        super().__init__(cluster)

        self.set_options({
            "snake_len": snake_len,
            "bg_color": bg_color,
            "snake_color": snake_color
        })

        # save loop in var so it doesnt restart each time (first iter is fired automatically,
        # but it starts from 0 so we dont notice)
        self._steps = self._step_loop()


    # prepare infinite frames (it is an iterable)
    def _step_loop(self):
        while True:
            for strip in self.cluster.strips_used:
                self.cluster.fill(self.options["bg_color"])

                snake_len = self.options["snake_len"]
                for i in range(snake_len - 1, strip.len - snake_len - 1):
                    for j in range(snake_len):
                        strip.set(i + j, self.options["snake_color"])
                        strip.set(i - j, self.options["bg_color"])
                    yield 0 # retain loop and do one step every time


