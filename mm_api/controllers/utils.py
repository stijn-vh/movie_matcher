
class Utils():
    def clean_data(self, x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''
            
    def concat_features(self, x, features):
        parts = []
        for f in features:
            val = x[f]
            if isinstance(val, list):
                parts.append(' '.join(val))
            else:
                parts.append(val)
        return ' '.join(parts)