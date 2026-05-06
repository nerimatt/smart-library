# base class where every animation has to inherit from
class Animation:
    _animation_speed: int = 4 # 0 < x < 100 #NOTE: percentage of how much the color changes every frame
    _steps = None
    options: dict = None # dictionary, diff for each animation

    def set_options(self, opt = None):
        if opt != None:
            self.options = opt

    def modify_option(self, key, value):
        if key in self.options.keys():
            self.options[key] = value

    def step(self):
        return -1 # must be implemented
