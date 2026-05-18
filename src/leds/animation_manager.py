from logger import Logger

from src.leds.LED_cluster import LED_cluster, LED_segment
from src.leds.animations.fade import fade_animation
from src.leds.animations.rainbow import rainbow_animation
from src.leds.animations.led_chase import led_chase_animation

from time import sleep


class AnimationManager:

    animating = False
    current_animation = None

    # animations idx in array
    FADE = 0
    RAINBOW = 1
    LED_CHASE = 2

    def __init__(self, logger: Logger, cluster: LED_cluster, conf):
        self.logger = logger
        self.cluster = cluster

        # initialize all animations to be ran, they are a class with method step as one frame
        # every function must only execute one frame per function call
        # save in array so if you switch to another animation and back to this it saves it
        self.animations = [
            fade_animation(cluster, conf["led_strips"]["default_color"], False),
            rainbow_animation(cluster),
            led_chase_animation(cluster),
        ]

    def set_animation(self, animation_enum: int, animation_options: dict = None):
        if not (0 <= animation_enum < len(self.animations)):
            self.logger.Error("selected animation does not exist")
            return

        self.logger.Debug(f"led cluster animation set to: {animation_enum}")
        self.current_animation = self.animations[animation_enum]
        self.animating = True

        if animation_options != None:
            self.current_animation.set_options(animation_options)

    def pause_animation(self):
        self.animating = False
        self.logger.Info("led cluster animations paused")

    def resume_animation(self):
        self.animating = True
        self.logger.Info("led cluster animations resumed")

    def stop_animation(self):
        self.animating = False
        self.current_animation = None # progress saved in animations array
        self.logger.Info("led cluster animations stopped")

    # perform one frame of the selected animation
    # NOTE: the cluster is updated in main, outside of this, in case some other changes are made
    def step(self):
        if not self.animating:
            return

        if self.current_animation == None:
            self.logger.Error("no animation selected")
            return

        res = self.current_animation.step()

        if res == -1:
            self.logger.Error("error in animation")
            return



if __name__ == "__main__":
    import leds
    from config import conf_load

    logger = Logger()

    conf = conf_load()

    cluster = leds.cluster_create(conf)
    cluster_animation_manager = AnimationManager(logger, cluster, conf)


    cluster_animation_manager.set_animation(AnimationManager.FADE)
    # cluster_animation_manager.set_animation(AnimationManager.RAINBOW)
    # cluster_animation_manager.set_animation(AnimationManager.LED_CHASE)

    while True:
        cluster_animation_manager.step()
        cluster.update()

        sleep(1 / conf["fps"])
