from ..LED_cluster import LED_cluster

# base class where every animation has to inherit from
class Animation:
    _animation_speed: int = 100 # 0 < x <= 100 percentage of how much the color changes every frame
    _max_brightness: int = 128 # 0 < x <= 256

    _steps = None # loop iterator to be implemented animation specific
    options: dict = dict() # different for each animation
    id: str

    cluster: LED_cluster

    def __init__(self, id: str, cluster: LED_cluster):
        self.id = id
        self.cluster = cluster

    def step(self):
        return next(self._steps)

    # this will add on top of existing options,
    # if option is already set it will override it
    def set_options(self, opt: dict = None):
        if opt == None: return

        for key in opt.keys():
            self.options[key] = opt[key]

    def modify_option(self, key, value):
        if key in self.options.keys():
            self.options[key] = value

    def check_id(self, id: str):
        return id == self.id
