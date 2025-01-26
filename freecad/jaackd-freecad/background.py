import logging
import schedule
import threading
import time
import inspect
from config.config_manager import ConfigManager

class BackgroundProcessor:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.jobs = []
        self.job_functions = {}
        self.job_run_counts = {}
        self.load_jobs()
        self.logger = logging.getLogger(__name__)

    def load_jobs(self):
        self.jobs = self.config_manager.get_jobs() or []
        for job in self.jobs:
            name = job['name']
            code = job['code']
            self.job_functions[name] = self.create_function_from_code(code)
            self.job_run_counts[name] = 0

    def save_jobs(self):
        self.config_manager.update_jobs(self.jobs)

    def reload_jobs(self):
        schedule.clear()
        self.load_jobs()
        self.start()

    def start(self):
        for job in self.jobs:
            name = job['name']
            interval = job['interval']
            if job.get('active', True):
                schedule.every(interval).seconds.do(self.run_job, name).tag(name)

        thread = threading.Thread(target=self.run_scheduler)
        thread.daemon = True
        thread.start()
        logging.info("Background processor started")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_job(self, job_name):
        self.logger.info(f"Running job: {job_name}")
        # Execute the job-specific function
        if job_name in self.job_functions:
            self.job_functions[job_name]()
            self.job_run_counts[job_name] += 1
            # Check if the job has reached its max_runs
            for job in self.jobs:
                if job['name'] == job_name and 'max_runs' in job:
                    if self.job_run_counts[job_name] >= job['max_runs']:
                        self.logger.info(f"Job {job_name} has reached its max_runs and will be deactivated.")
                        schedule.clear(job_name)
                        job['active'] = False
                        self.save_jobs()

    def add_job(self, name, interval, func, max_runs=None):
        """
        Add a new job to the background processor.

        Args:
            name (str): The name of the job.
            interval (int): The interval in seconds at which the job should run.
            func (callable): The function or lambda to execute for the job.
            max_runs (int, optional): The maximum number of times the job should run.
        """
        # Extract the source code of the lambda function
        code = inspect.getsource(func).strip()
        # Add the job to the schedule
        schedule.every(interval).seconds.do(self.run_job, name).tag(name)
        self.logger.info(f"Added new job: {name} with interval: {interval} seconds")

        # Update the jobs list and save the configuration
        job = {'name': name, 'interval': interval, 'code': code, 'active': True}
        if max_runs is not None:
            job['max_runs'] = max_runs
        self.jobs.append(job)
        self.job_functions[name] = func
        self.job_run_counts[name] = 0
        self.save_jobs()

    def create_function_from_code(self, code):
        """
        Create a function from the given code string.

        Args:
            code (str): The code to execute.

        Returns:
            callable: The function created from the code.
        """
        def func():
            exec(code)
        return func

    def activate_job(self, name):
        """
        Activate a job by name.

        Args:
            name (str): The name of the job to activate.
        """
        for job in self.jobs:
            if job['name'] == name:
                job['active'] = True
                schedule.every(job['interval']).seconds.do(self.run_job, name).tag(name)
                self.save_jobs()
                self.logger.info(f"Activated job: {name}")
                break

    def deactivate_job(self, name):
        """
        Deactivate a job by name.

        Args:
            name (str): The name of the job to deactivate.
        """
        for job in self.jobs:
            if job['name'] == name:
                job['active'] = False
                schedule.clear(name)
                self.save_jobs()
                self.logger.info(f"Deactivated job: {name}")
                break

# Usage example:
# config_manager = ConfigManager()
# processor = BackgroundProcessor(config_manager)
# processor.start()
# processor.add_job("new_job", 15, lambda: print("Running new job"), max_runs=5)
# processor.deactivate_job("new_job")
# processor.activate_job("new_job")