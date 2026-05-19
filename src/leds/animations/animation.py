from ..LED_cluster import LED_cluster

# base class where every animation has to inherit from
class Animation:
    # TODO: move in options?
    _animation_speed: int = 100 # 0 < x <= 100 percentage of how much the color changes every frame
    _max_brightness: int = 255 # 0 < x <= 255

    _steps = None # loop iterator to be implemented animation specific options: dict = dict() # different for each animation id: str

    options: dict = dict()
    id: str

    cluster: LED_cluster

    def __init__(self, id: str, cluster: LED_cluster):
        self.id = id
        self.cluster = cluster

        # save loop in var so it doesnt restart each time (first iter is fired automatically,
        # but it starts from 0 so we dont notice)
        self._steps = self._step_loop()

    # NOTE: animation loop is here, this is the format, automatically steps
    def _step_loop(self):
        while True:
            yield 0

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

    def state_export(self):
        # export settings and animatino speend and max brihjtness and some global var
        pass

    def state_import(self, state: dict):
        pass
