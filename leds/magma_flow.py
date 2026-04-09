from time import sleep

from RGBSTRIP import RGBSTRIP

strip = RGBSTRIP(data_pin = 27, n_leds = 20)

palette = (
    (255, 37, 0),
    (255, 102, 0),
    (242, 242, 23),
    (234, 92, 15),
    (229, 101, 32)
)


def magma_flow(strip, head_distance = 5):
    """ WILL RUN IN A INFINTIE WHILE LOOP
    head_distance: distance the head has to travel in the animation -> is subsequently total frames of animation
    """
    # NOTE: shift hue from a red / orange to a orange / yellow randomized and not necessarely in order

    n_heads = strip.len / head_distance
    
    # colors
    main_col = (255, 0, 0)

    
    for frame in range(head_distance):
        strip.fill((0, 0, 0))
        for head in range(n_heads):
            head_pos = head * head_distance + frame

            # fill heads
            strip.set(head_pos, palette[0]) 

            yellow_intensity_step = 100 / head_distance * 0.01
            yellow_intensity_percentage = 0 # 0 - 1

            # fill after led
            for after_pos in range(head_distance - 1 - frame):
                #print(yellow_intensity_percentage)
                strip.set(head_pos + 1 + after_pos, palette[1])
                yellow_intensity_percentage += yellow_intensity_step

            # fill before led
            for before_pos in range(frame):
                #print(yellow_intensity_percentage)
                strip.set(head_pos -  before_pos - 1, palette[2])
                yellow_intensity_percentage += yellow_intensity_step
        

        strip.write()

        sleep(0.1)

if __name__ == "__main__":
    while True:
        magma_flow(strip = strip)
