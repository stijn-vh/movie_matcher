class DataValidator:
    def check_multiple(self, data, keys):
        for key in keys:
            if key[0] not in data or isinstance(data[key[0]], key[1]):
                return False
        return True