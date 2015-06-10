__author__ = 'Conor'

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Algorithm(object):

    # Initialize the algorithm
    def __init__(self):
        self.heuristic_weighting = {}  # TODO - Add multiple heuristics with possibility for weightings
