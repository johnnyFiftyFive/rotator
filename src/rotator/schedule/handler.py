from rotator import scheduler


def modify_job(job_id, hours='*', minutes='*'):
    scheduler.modify_job(job_id, hour=hours, minute=minutes)


def halt_job(job_id):
    if is_job_running(job_id):
        scheduler.pause_job(job_id)


def resume_job(job_id):
    if not is_job_running(job_id):
        scheduler.resume_job(job_id)


def is_job_running(job_id):
    job = scheduler.get_job(job_id)
    return job.next_run_time is not None
