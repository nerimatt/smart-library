from leds.LED_strip import LED_strip
from leds.LED_cluster import LED_cluster, LED_segment

def cluster_create(config) -> LED_cluster:
    segment_length = 20
    segments_per_strip = 8

    PIN_STRIP_1 = config["led_strips"]["pin_1"]
    PIN_STRIP_2 = config["led_strips"]["pin_2"]


    strip = LED_strip(data_pin = PIN_STRIP_1, n_leds = segments_per_strip * segment_length)
    strip2 = LED_strip(data_pin = PIN_STRIP_2, n_leds = segments_per_strip * segment_length)

    # must follow order in which the led strips are placed in the blocks
    def seg(library_block_IDX, strip = strip):
        return LED_segment(strip, segment_length * library_block_IDX, segment_length)

    # matrix rappresentation of the library leds, each segment is a block
    leds = [
        seg(1), None, seg(0),
        seg(2), seg(3), seg(4),
        seg(7), seg(6), seg(5),
        seg(0, strip2), seg(1, strip2), None,
        None, None, None,
        None, None, None,
    ]

    return LED_cluster(leds, 3, [strip, strip2], config["led_strips"]["default_color"])


def cluster_blink(cluster: LED_cluster, iterations: int):
    interval = 0.5

    cluster.off()

    for _ in range(iterations):
        cluster.fill(cluster.default_color).update()
        sleep(interval)

        cluster.off()
        sleep(interval)


