class Convert:
    def to_dict(self, obj):
        if isinstance(obj, dict):
            return {key: self.to_dict(value) for key, value in obj.items() if key != 'isObject'}
        elif hasattr(obj, '__dict__'):
            return {key: self.to_dict(value) for key, value in obj.__dict__.items() if key != 'isObject'}
        elif isinstance(obj, list):
            return [self.to_dict(item) for item in obj]
        else:
            return obj