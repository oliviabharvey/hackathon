import yaml
import time
from copy import deepcopy

from utils.enums import TimeStamps


TRIAL_SCHEMA = {
    'success': None,
    'rewarded': None,
    'seconds_between_display_and_touch': None,
    'seconds_between_feed_and_eat': None
    }

RESULTS_SCHEMA = {
    'trials': {},
    'summary': {}
    }  

class DataManager():

    def __init__(self, cfg):
        self.cfg = cfg
        # adding relevant keys from config to results dict
        self.data = {x: cfg[x] for x in cfg if x not in ['results']}
        # adding required keys from Results Schema
        self.data.update(RESULTS_SCHEMA)
        self.current_trial = 0

    def update(self, time_stamp_type, info=None):
        if time_stamp_type == TimeStamps.DISPLAY:
            self.trial_display_time_start = time.time()
        elif time_stamp_type == TimeStamps.TOUCH:
            self.data['trials'][self.current_trial]['seconds_between_display_and_touch'] = round(time.time() - self.trial_display_time_start, 1)
            self.data['trials'][self.current_trial]['success'] = info['success']
            self.data['trials'][self.current_trial]['rewarded'] = info['rewarded']
        elif time_stamp_type == TimeStamps.FEED:
            self.trial_feed_time_start = time.time()
        elif time_stamp_type == TimeStamps.EAT:
            self.data['trials'][self.current_trial]['seconds_between_feed_and_eat'] = round(time.time() - self.trial_feed_time_start, 1)

    def update_status(self, status):
        self.data['status'] = status

    def write_dict(self, path='results/results.yaml'):
        with open(path, "w") as file:
            yaml.dump(self.data, file, default_flow_style=False)

    def start_trial(self):
        self.current_trial += 1
        self.data['trials'][self.current_trial] = deepcopy(TRIAL_SCHEMA)
        return
