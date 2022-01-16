import time

import logging

from project.server.main.utils.db import db_aggregate
from project.server.main.utils.utils import f, get_worker_stats


def daily():
    start = time.perf_counter()
    print("TASK: daily started")
    logging.info("TASK: daily started")

    db_aggregate()

    worker_stats = get_worker_stats()
    print(worker_stats)
    logging.info(worker_stats)

    end = time.perf_counter()
    print("TASK: daily completed in " + str(f(end - start)) + "s")
    logging.info("TASK: daily completed in " + str(f(end - start)) + "s")
    return True
