import statistics
import time
import yaml
from copy import deepcopy
from typing import Dict

from utils.enums import TimeStamps


TRIAL_SCHEMA = {
    'success': None,
    'rewarded': None,
    'seconds_between_display_and_touch': None,
    'seconds_between_feed_and_eat': None
    }

SUMMARY_SCHEMA = {
    'total_time': None,
    'trials_number': None,
    'average_seconds_between_display_and_touch': None,
    'average_seconds_between_feed_and_eat': None,
    'number_of_reversals': None
    }

RESULTS_SCHEMA = {
    'trials': {},
    'summary': deepcopy(SUMMARY_SCHEMA)
    }  

class DataManager():
    """
    Calculating experiment statistics and generating outputs at each step of the experiment.
    """

    def __init__(self, cfg: Dict):
        self.cfg = cfg
        # adding relevant keys from config to results dict
        self.data = {x: cfg[x] for x in cfg if x not in ['results']}
        # adding required keys from Results Schema
        self.data.update(RESULTS_SCHEMA)
        self.current_trial = 0

    def update(self, time_stamp_type: int , info: Dict = None):
        """
        Update the data dictonnary during one of the 4 steps (dislay, touch, feed, eat)
        """
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

    def update_status(self, status: str):
        """
        Update the status string.
        
        Inputs:
            - status: string to output (ex: 'running', 'completed')
        """
        self.data['status'] = status

    def write_dict(self, path='results/results.yaml'):
        """
        Write the results to a YAML file.
        """
        with open(path, "w") as file:
            yaml.dump(self.data, file, default_flow_style=False)

    def start_trial(self):
        """
        Trial counter when a new image showing trial is showned.
        """
        self.current_trial += 1
        self.data['trials'][self.current_trial] = deepcopy(TRIAL_SCHEMA)
        return

    def compute_end_of_experiment_statistics(self, start_time, num_reversals):
        """
        Compute all the statistics useful for analysing the experiment.
        """
        self.data['summary']['total_time'] = round(time.time() - start_time, 1)
        self.data['summary']['trials_number'] = len(self.data['trials'])
        display_and_touch_times = []
        feed_and_eat_times = []
        for trial in self.data['trials']:
            if self.data['trials'][trial]['seconds_between_display_and_touch'] != None:
                display_and_touch_times.append(self.data['trials'][trial]['seconds_between_display_and_touch'])
            if self.data['trials'][trial]['seconds_between_feed_and_eat'] != None:
                feed_and_eat_times.append(self.data['trials'][trial]['seconds_between_feed_and_eat'])
        if display_and_touch_times:
            self.data['summary']['average_seconds_between_display_and_touch'] = round(statistics.mean(display_and_touch_times), 1)
        else:
            self.data['summary']['average_seconds_between_display_and_touch'] = -1
        if feed_and_eat_times:
            self.data['summary']['average_seconds_between_feed_and_eat'] = round(statistics.mean(feed_and_eat_times), 1)
        else:
            self.data['summary']['average_seconds_between_feed_and_eat'] = -1
        self.data['summary']['number_of_reversals'] = num_reversals