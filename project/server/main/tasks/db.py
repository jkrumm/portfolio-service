# project/server/main/portfolio.py


import time


def cleanData(db, tf):
    print("TASK: cleanData db: " + db + " // tf: " + tf)
    return True

def aggregate(db, tf):
    print("TASK: aggregate db: " + db + " // tf: " + tf)
    return True

def trigger_error_queue():
    division_by_zero = 1 / 0
    return True
