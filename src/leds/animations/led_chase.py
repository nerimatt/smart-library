from ..LED_cluster import LED_cluster

from .animation import Animation

class led_chase_animation(Animation):

    def __init__(self, cluster: LED_cluster, snake_len = 10, bg_color = (0, 0, 0), snake_color = (0, 0, 255), glow_radius = 15):
        super().__init__("led_chase", cluster)

        self.set_options({
            "snake_len": snake_len,
            "bg_color": bg_color,
            "snake_color": snake_color,
            "glow_radius": glow_radius,
        })

        # save loop in var so it doesnt restart each time (first iter is fired automatically,
        # but it starts from 0 so we dont notice)
        self._steps = self._step_loop()

    def _get_glow_color(self, col, distance_from_body):
        # for every pixel of distance away, decrement the colo by 1 / glow_radius (at the last one it becomes 0 (distance_from_body == glow_radius))
        # TODO: fix it to make it more apparent, for now i find difference only at 90% less
        # return [int(x - x * distance_from_body / glow_radius) for x in col]
        return [int(x * 0.05) for x in col]

    def _step_loop(self):

        while True:
            for i in range(self.cluster.len_flat):

                snake_len = self.options["snake_len"]

                # animate snake, every frame add one forward and remove one back of the snake
                self.cluster.set_flat(i, self.options["snake_color"]) # head

                # create glow of 5 blocks around snake
                # glow on front
                for j in range(self.options["glow_radius"]):
                    if i + j + 1 < self.cluster.len_flat:
                        self.cluster.set_flat(i + j + 1, self._get_glow_color(self.options["snake_color"], j + 1))

                    if i - snake_len - j > 0:
                        self.cluster.set_flat(i - snake_len - j, self._get_glow_color(self.options["snake_color"], j + 1))



                # chop off end of glow (start if absorbed automatically)
                if (i - snake_len - self.options["glow_radius"] > 0):
                    self.cluster.set_flat(i - snake_len - self.options["glow_radius"], self.options["bg_color"])
                else:
                    # TODO: remove from end
                    pass



                yield 0 # retain loop and do one step every time


