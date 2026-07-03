import time


class MarketScheduler:

    def __init__(self):

        self.tasks = []

    def add_task(

        self,

        name,

        interval,

        callback

    ):

        self.tasks.append({

            "name": name,

            "interval": interval,

            "callback": callback,

            "last_run": 0

        })

    def run(self):

        now = time.time()

        for task in self.tasks:

            if now - task["last_run"] >= task["interval"]:

                task["callback"]()

                task["last_run"] = now
