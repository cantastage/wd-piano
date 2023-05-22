from typing import Dict
from model.settings import Settings


class Utils(object):

    _instance = None  # singleton instance

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(Utils, cls).__new__(cls)
        return cls._instance

    @classmethod
    def parse_simulation_settings(cls, settings: Dict) -> Dict:
        settings['hammerMass'] = settings['hammerMass'] / 1000  # convert from grams to kilograms
        settings['stringLength'] = settings['stringLength'] / 100  # convert from cm to m
        settings['stringDiameter'] = settings['stringDiameter'] / 1000  # convert from millimeters to meters
        settings['hammerStringDistance'] = settings['hammerStringDistance'] / 100  # convert from cm to m
        return settings




