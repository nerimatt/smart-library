# base class where every animation has to inherit from
class Animation:
    _animation_speed: int = 4 # 0 < x < 100 #NOTE: percentage of how much the color changes every frame
    _steps = None

    def step(self):
        return -1 # must be implemented
