#!/usr/bin/env python3

import os
import time
import logging
import numpy as np
from numpy import loadtxt
import cProfile
import random
import ray

if ray.is_initialized:
    ray.shutdown()
ray.init(logging_level=logging.ERROR)

# Excercises 1.1)
# Try using local bubble sort and remote bubble sort,
# show difference

def bubble_sort(arr):
  n = len(arr)
  for i in range(n):
    for j in range(1, n - i):
      if arr[j - 1] > arr[j]:
        arr[j - 1], arr[j] = arr[j], arr[j - 1]

def gen_random_array(sz):
  return [random.randint(-100, 100) for _ in range(sz)]

def sort_arrs(no: int):
  for _ in range(no):
    arr = gen_random_array(100)
    bubble_sort(arr)

def sort_local(no):
  sort_arrs(no)

@ray.remote
def sort_remote(no):
  sort_arrs(no)

print("local run")
cProfile.run("sort_local(1000)")

print("remote run")
cProfile.run("sort_remote.remote(1000)")

ray.shutdown()

