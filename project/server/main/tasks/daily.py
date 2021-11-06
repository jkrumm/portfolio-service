# project/server/main/portfolio.py

# send reports to telegram bot

# Worker Statistics - https://python-rq.org/docs/workers/
# If you want to check the utilization of your queues, Worker instances store a few useful information:
#
# from rq.worker import Worker
# worker = Worker.find_by_key('rq:worker:name')
#
# worker.successful_job_count  # Number of jobs finished successfully
# worker.failed_job_count # Number of failed jobs processed by this worker
# worker.total_working_time  # Amount of time spent executing jobs (in seconds)

def daily():
    print("TASK: daily")
    i = 1 / 0
    return True
