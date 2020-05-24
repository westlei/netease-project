import confuse
class Config(object):
    config = None
    """The confuse.Configuration object."""

    def __init__(self):
        """The config constructor should be called only once."""
        if self.config is None:
            self.config = confuse.Configuration("PandasProfiling", __name__)
            self.config.set_file('./pandas_profiling/config.yaml')

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, key, value):
        self.config[key].set(value)

config = Config()
