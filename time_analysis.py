__author__ = 'Conor'

import main
import logging
import operator
import algorithm

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

num_test_runs = 10000
g = main.Game()

a = algorithm.Algorithm()


def time_test(function_name, *args):
    getattr(g, function_name)(*args)


def tree_time_test():
    getattr(a, 'run')


def run_time_test_on_function(function_name, *args):
    import timeit

    logger.critical("Running %s calls of %s...", num_test_runs, function_name)
    function_string = "time_test('{}')" if len(args) == 0 else "time_test('{}','{}')"
    total_time = timeit.timeit(function_string.format(function_name, *args), setup="from __main__ import time_test",
                               number=num_test_runs)

    return total_time


def run_main_time_tests():
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
        logger.critical("     - Average calls completed per second:     %s",
                        "{:,}".format(round(num_test_runs / result[1], 2)))
        # logger.critical("   --  Average seconds per call:               %s", round(result[1] / num_test_runs), 2)
        logger.critical("")


def time_fn(fn, *args, **kwargs):
    import time

    start = time.clock()
    results = getattr(a, fn)(*args, **kwargs)
    end = time.clock()
    total_time = round(end - start, 2)

    # print fn + ": " + str(total_time) + " s"
    #
    logger.critical("Total time:: %s seconds", str(total_time))
    logger.critical("   ")

    return args[0], results, total_time


def run_decision_tree_generation_time_test(levels_to_search):
    results = []

    for x in range(levels_to_search):
        results.append(time_fn('run', x + 1))

    logger.critical("   ")
    logger.critical("------------------------------ ::: TEST RESULTS ::: --------------------------------------")
    for result in results:
        logger.critical("   ::  Decision tree of depth %s", result[0])
        logger.critical("   ::  Created [%s] nodes in [%s] seconds", result[1], result[2])
        if not result[2] == 0.0:
            logger.critical("   ::  Average of [%s] nodes generated per second", round(result[1] / result[2], 2))
        logger.critical("   ")

    get_number_of_calls_for_functions(main.Game())


def get_number_of_calls_for_functions(class_instance):
    import inspect

    logger.critical("   ")
    logger.critical("------------------------------ ::: TEST RESULTS ::: --------------------------------------")
    logger.critical("   ")

    functions = inspect.getmembers(class_instance, predicate=inspect.ismethod)
    function_total_time = {}
    function_count = {}
    for fn in functions:
        function_total_time[fn[0]] = fn[1].total_time
        function_count[fn[0]] = fn[1].called
        # logger.critical("%s calls: %s", fn[0], fn[1].called)

    readable_function_count = sorted(function_total_time.items(), key=operator.itemgetter(1), reverse=True)
    for x in readable_function_count:
        logger.critical("-------::  Function: %s  ::  ", x[0])
        logger.critical("       ::  [%s] seconds", round(x[1], 3))
        logger.critical("       ::  [%s] calls", function_count[x[0]])
        if not x[1] == 0.0:
            logger.critical("       ::  [%s] calls per second", round(function_count[x[0]] / x[1], 4))
        logger.critical("       ")


if __name__ == '__main__':
    # Tests for main
    # run_main_time_tests()

    # Tests for Decision Tree Generation
    run_decision_tree_generation_time_test(3)

    # TODO - Put tests for alpha beta pruning
    ##############
