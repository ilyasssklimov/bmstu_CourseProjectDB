class BaseModel:
    def __init__(self, **kwargs):
        self._args = kwargs
        if 'id' not in self._args:
            raise KeyError('Key \'id\' must be in param dictionary')
        for arg in self._args:
            self.__getter_setter(arg)

    @staticmethod
    def __getter_setter(name):
        setattr(BaseModel, name, property(lambda self: self._args[name]))
        setattr(BaseModel, f'set_{name}', lambda self, value: self.__setitem__(name, value))

    def get_params(self):
        return list(self._args.values())

    def get_names(self):
        return list(self._args.keys())

    def get_params_dict(self):
        return self._args

    def __getitem__(self, item):
        if item in self._args:
            return self._args[item]
        else:
            return None

    def __setitem__(self, key, value):
        if not isinstance(key, str) or key not in self._args:
            raise ValueError(f'there is not key \'{key}\' in the model \'{self.__class__.__name__}\'')
        self._args[key] = value

    def __len__(self):
        return len(self._args)

    def __bool__(self):
        return self._args['id'] != -1

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'{type(self).__name__} ({self._args})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.get_names() == other.get_names() and self.get_params() == other.get_params()
