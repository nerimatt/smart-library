# controls multiple RGBSTRIP at once

from LED_STRIP import LED_STRIP

class LED_segment:
    def __init__(self, strip: LED_STRIP, idx_start: int, len: int) -> None:

        if strip.len < idx_start + len:
            print("cannot create segment, it will go out of bounds")
            return

        self.strip = strip
        self.idx_start = idx_start # from which led we need to start segment
        self.len = len # how long is our segment

    def fill(self, col = (0, 0, 0)) -> LED_segment:
        for i in range(self.len):
            self.strip.set(i, col)
        return self

    def set(self, idx, col = (0, 0, 0)):
        if not (0 <= idx <= self.len):
            print("LED SEGMENT out of bounds index in set")
            return self

        self.strip.set(idx, col)
        return self





class LED_cluster:
    def __init__(self, led_matrix_array: list[LED_segment], row_length: int, strips_used : list[LED_STRIP]) -> None:
        self.leds = led_matrix_array
        self.strips_used = strips_used

        self.width = row_length # how many blocks is one row
        self.height = len(self.leds) / self.width

    def fill(self, col = (0, 0, 0)) -> LED_cluster:
        for strip in self.strips_used:
            strip.fill(col)
        return self

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
    segment_length = 20
    segments_per_strip = 8

    PIN_STRIP_1 = 12
    PIN_STRIP_2 = 13

    strip = LED_STRIP(data_pin = PIN_STRIP_1, n_leds = segments_per_strip * segment_length)
    strip2 = LED_STRIP(data_pin = PIN_STRIP_2, n_leds = segments_per_strip * segment_length)

    # must follow order in which the led strips are placed in the blocks
    def seg(library_block_IDX, strip = strip):
        return LED_segment(strip, segment_length * library_block_number, segment_length)

    # matrix rappresentation of the library leds, each segment is a block
    leds = [
        seg(1), None, seg(0),
        seg(2), seg(3), seg(4),
        seg(7), seg(6), seg(5),
        seg(8, strip2), seg(9, strip2), None,
        None, None, None,
        None, None, None,
    ]

    cluster = LED_cluster(leds, 3, [strip, strip2])
    cluster.set(2, 0, (255, 0, 0))
