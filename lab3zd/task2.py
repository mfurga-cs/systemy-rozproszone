#!/usr/bin/env python3

import logging
import numpy as np
import ray
import sys
import random

# Excercises 2.1) Create large lists and python dictionaries,
# put them in object store. Write a Ray task to process them.

if ray.is_initialized:
    ray.shutdown()
ray.init(logging_level=logging.ERROR)

def gen_random_array(sz):
  return [random.randint(0, 100) for _ in range(sz)]

def gen_random_dict(sz):
  return { i: i ** 2 for i in range(sz) }

@ray.remote
def array_sum(arr1, arr2):
  assert len(arr1) == len(arr2)
  r = []
  n = len(arr1)
  for i in range(n):
    r.append(arr1[i] + arr2[i])
  return r

@ray.remote
def dict_mul(dict1, dict2):
  assert len(dict1) == len(dict2)
  r = dict()
  n = len(dict1)
  for i in range(n):
    r[i] = dict1[i] * dict2[i]
  return r

arr1 = gen_random_array(10)
arr2 = gen_random_array(10)
arr1_ref = ray.put(arr1)
arr2_ref = ray.put(arr2)

dict1 = gen_random_dict(10)
dict2 = gen_random_dict(10)
dict1_ref = ray.put(dict1)
dict2_ref = ray.put(dict2)

r1 = array_sum.remote(arr1_ref, arr2_ref)
r2 = dict_mul.remote(dict1_ref, dict2_ref)

print(arr1)
print(arr2)
print(ray.get(r1))

print()

print(dict1)
print(dict2)
print(ray.get(r2))

ray.shutdown()

