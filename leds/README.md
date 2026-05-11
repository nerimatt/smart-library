# LEDS

colors with leds are strange. (0, 0, 0) is black, which is the off state. but if black is off then we cant have grey colors, so it results in the colors being more dimmed

looking at these two colors, (255, 191, 0) == (4, 3, 0), the proportions are the same, the second color is tecnically mixed with black,
so what we will get is simply the same color, just a lot more dimmed

knowing this, color * 0.5 will make it ~50% less powerful, but still retain its color. this of course must be taken with a pinch of salt, as how leds are not perfect
