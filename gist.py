import json

class Gist (dict):
    def __init__ (self, description):
        super(Gist, self).__init__()
        self['description'] = description
        self['files'] = {}

        self.order = []

    def add(self, name, content):
        self.order.append(name)
        self['files'][name] = {'content': content}

    def filenames(self):
        return self.order

    def to_json(self):
        return json.dumps(self, indent=2)

def anchor(filename):
    return 'file-' + filename.replace('.', '-')

