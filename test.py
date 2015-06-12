__author__ = 'Conor'

import main
import logging

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

num_test_runs = 10000


def test():
    g = main.Game()
    logging.critical("Starting %s calls of Game.get_all_possible_moves()...", num_test_runs)
    for n in range(1, num_test_runs + 1):
        g.get_all_possible_moves()

if __name__ == '__main__':
    import timeit

    # Disable logging to speed up calls
    logging.disable(logging.INFO)
    #  TODO - Figure out if the performance decrease of logging to console (pretty big) is similar to logging to file

    total_time_all_possible_moves = timeit.timeit("test()", setup="from __main__ import test", number=1)
    logger.critical("------------------------------ ::: TEST RESULTS ::: --------------------------------------")
    logger.critical("Total seconds to run all_possible_moves %s times: %s", num_test_runs,
                    str(total_time_all_possible_moves))
    logger.critical("Average calls per second: %s", num_test_runs / total_time_all_possible_moves)
    logger.critical("Average seconds per call: %s", total_time_all_possible_moves / num_test_runs)
