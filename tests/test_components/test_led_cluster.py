import leds
import time
import config

cluster = leds.cluster_create(config.conf_load())
print(cluster.leds)


nsegs = len(cluster.leds)
for idx, seg in enumerate(cluster.leds):
    if not seg: continue

    seg.fill((
        int(255 * (nsegs - idx)/ nsegs),
        int (255 * idx / nsegs),
        0
    ))
    cluster.update()
    time.sleep(1)
    seg.off()


cluster.off()
