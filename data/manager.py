import yaml

class DataManager():

    def __init__(self, cfg):
        self.cfg = cfg
        self.data = {}

    def update(self):
        return

    def update_status(self, status):
        self.data['status'] = status

    def write_dict(self, path='results/results.yaml'):
        with open(path, "w") as file:
            yaml.dump(self.data, file, default_flow_style=False)


