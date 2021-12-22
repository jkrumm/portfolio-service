import logging


def cleanData(db, tf):
    print("TASK: cleanData db: " + db + " // tf: " + tf)
    logging.info("TASK: cleanData db: " + db + " // tf: " + tf)
    return True


def aggregate(db, tf):
    print("TASK: aggregate db: " + db + " // tf: " + tf)
    logging.info("TASK: aggregate db: " + db + " // tf: " + tf)
    return True


def trigger_error_queue():
    print("TASK: trigger_error_queue")
    logging.info("TASK: trigger_error_queue")
    division_by_zero = 1 / 0
    return True
