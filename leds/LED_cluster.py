# controls multiple RGBSTRIP at once

from time import sleep

from leds.LED_strip import LED_strip

class LED_segment:
    def __init__(self, strip: led_strip, idx_start: int, len: int) -> None:

        if strip.len < idx_start + len:
            print(f"cannot create segment, it will go out of bounds, strip length {strip.len} at {idx_start} for {len} leds")
            return

        self.strip = strip
        self.idx_start = idx_start # from which led we need to start segment
        self.len = len # how long is our segment

    def fill(self, col = (0, 0, 0)) -> LED_segment:
        for i in range(self.len):
            self.strip.set(self.idx_start + i, col)
        return self

    def off(self):
        self.fill((0, 0, 0))

    def set(self, idx, col = (0, 0, 0)):
        if not (0 <= idx <= self.len):
            print("LED SEGMENT out of bounds index in set")
            return self

        self.strip.set(self.idx_start + idx, col)
        return self





class LED_cluster:
    def __init__(self, led_matrix_array: list[LED_segment], row_length: int, strips_used : list[led_strip], default_color = (255, 255, 255)) -> None:
        self.leds = led_matrix_array
        self.strips_used = strips_used

        self.width = row_length # how many blocks is one row
        self.height = len(self.leds) / self.width

        self.default_color = default_color

    def fill(self, col = (0, 0, 0)) -> LED_cluster:
        for strip in self.strips_used:
            strip.fill(col)
        return self

    def off(self): #NOTE: automatically updates in strip.off()
        for strip in self.strips_used:
            strip.off()

    def update(self):
        for strip in self.strips_used:
            strip.update()

    def set(self, x: int, y: int, col = (0, 0, 0)):
        if not (0 <= y < self.height or 0 <= x < self.width) :
            print("LED CLUSTER error, in set x or y is out of bounds")
            return self


        # check whole row segments_per_strip to find the x pos
        explored_x = 0
        seg = None
        for seg_idx in range(self.width):
            seg = self.leds[y * self.height + seg_idx]
            if seg == None: continue

            if seg.len + explored_x > x:
                # we found the segment
                seg.set(x - explored_x, col)
                break

            explored_x += seg.len


        return self



if __name__ == "__main__":
    import config

    conf = config.conf_load()

    cluster = cluster_create(conf)
    cluster_blink(cluster, 3)
