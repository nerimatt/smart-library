# controls multiple RGBSTRIP at once

from RGBSTRIP import RGBSTRIP

class LED_segment:
    def __init__(self, strip, idx_start, led_count):
        self.strip = strip
        self.idx_start = idx_start # from which led we need to start segment
        self.led_count = led_count # how long is our segment

class LED_cluster:
    def __init__(self, led_matrix_array):
        pass


if __name__ == "__main__":
    segment_length = 20
    segments = 8

    PIN_STRIP_1 = 12
    PIN_STRIP_2 = 13

    strip = RGBSTRIP(data_pin = PIN_STRIP_1, n_leds = segments * segment_length)
    strip2 = RGBSTRIP(data_pin = PIN_STRIP_2, n_leds = segments * segment_length)

    # must follow order in which the led strips are placed in the blocks
    def seg(library_block_IDX, strip = strip):
        return LED_segment(strip, segment_length * library_block_number, segment_length)

    # matrix rappresentation of the library leds, each segment is a block
    leds = [
        seg(1), NULL, seg(0),
        seg(2), seg(3), seg(4),
        seg(7), seg(6), seg(5),
        seg(8, strip2), seg(9, strip2), NULL,
        NULL, NULL, NULL,
        NULL, NULL, NULL,
    ]
