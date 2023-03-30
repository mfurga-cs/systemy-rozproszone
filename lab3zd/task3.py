#!/usr/bin/env python3

import logging
import time
import ray
import random
import math
import numpy as np
from random import randint
from fractions import Fraction

if ray.is_initialized:
    ray.shutdown()
ray.init(logging_level=logging.ERROR)

# excercise 3
# 3.0 start remote cluster settings and observe actors in cluster
# a) make screenshot of dependencies
# 3.1. Modify the Actor class MethodStateCounter and add/modify methods that return the following:
# a) - Get number of times an invoker name was called
# b) - Get a list of values computed by invoker name
# 3- Get state of all invokers
# 3.2 Modify method invoke to return a random int value between [5, 25]

# 3.3 Take a look on implement parralel Pi computation
# based on https://docs.ray.io/en/master/ray-core/examples/highly_parallel.html
#
# Implement calculating pi as a combination of actor (which keeps the
# state of the progress of calculating pi as it approaches its final value)
# and a task (which computes candidates for pi)


@ray.remote
class Worker:
  def __init__(self, times: int):
    self.times = times
    self.count = 0

  def work(self):
    for _ in range(self.times):
      x = random.random()
      y = random.random()
      if x * x + y * y <= 1:
        self.count += 1
    return Fraction(self.count, self.times)

@ray.remote
class Supervisor:
  def __init__(self, times, workers):
    self.workers = [Worker.remote(times) for _ in range(workers)]

  def start(self):
    result = [worker.work.remote() for worker in self.workers]
    result = ray.get(result)
    return sum(result) * 4 / len(result)

supervisor = Supervisor.remote(times=1000, workers=100)
result = supervisor.start.remote()

pi = float(ray.get(result))
diff = abs(pi - math.pi) / pi
print(f"pi = {pi}")
print(f"diff = {diff}")


