__author__ = 'Conor'

import main
import logging
import operator

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

num_test_runs = 10000
g = main.Game()


def time_test(function_name, *args):
    getattr(g, function_name)(*args)


def run_time_test_on_function(function_name, *args):
    import timeit

    logger.critical("Running %s calls of %s...", num_test_runs, function_name)
    function_string = "time_test('{}')" if len(args) == 0 else "time_test('{}','{}')"
    total_time = timeit.timeit(function_string.format(function_name, *args), setup="from __main__ import time_test",
                               number=num_test_runs)

    return total_time


def run_time_tests():
    logger.critical("Starting timeit tests...")
    # Disable logging to speed up calls
    logging.disable(logging.INFO)
    # TODO - Figure out if the performance decrease of logging to console (pretty big) is similar to logging to file
    # TODO - Figure out a more accurate way to assess the performance of the program as a whole

    test_space = 'b2'

    test_results = {}

    test_results['get_all_possible_moves'] = run_time_test_on_function('get_all_possible_moves')
    test_results['get_possible_moves_for_space'] = run_time_test_on_function('get_possible_moves_for_space', test_space)
    test_results['is_valid_space'] = run_time_test_on_function('is_valid_space', test_space)
    test_results['_get_possible_moves_horizontal'] = run_time_test_on_function('_get_possible_moves_horizontal',
                                                                               test_space)
    test_results['_get_possible_moves_vertical'] = run_time_test_on_function('_get_possible_moves_vertical', test_space)
    test_results['_get_possible_moves_diagonal'] = run_time_test_on_function('_get_possible_moves_diagonal', test_space)
    test_results['is_occupied_by_teammate'] = run_time_test_on_function('is_occupied_by_teammate', test_space)
    test_results['change_player'] = run_time_test_on_function('change_player')
    test_results['__str__'] = run_time_test_on_function('__str__')

    # make a list of tuples sorted by total run time for each function
    readable_test_results = sorted(test_results.items(), key=operator.itemgetter(1), reverse=True)

    logger.critical("------------------------------ ::: TEST RESULTS ::: --------------------------------------")
    for result in readable_test_results:
        logger.critical("   :: %s :: ", result[0])
        logger.critical("     - Total seconds for %s calls:         %s", num_test_runs, round(result[1], 5))
        logger.critical("     - Average calls completed per second:     %s", "{:,}".format(round(num_test_runs / result[1], 2)))
        # logger.critical("   --  Average seconds per call:               %s", round(result[1] / num_test_runs), 2)
        logger.critical("")


if __name__ == '__main__':
    # Tests for main
    run_time_tests()

    # TODO - Put tests for decision tree generation
    ##############

    # TODO - Put tests for alpha beta pruning
    ##############


