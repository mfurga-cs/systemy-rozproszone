#!/bin/bash

g++ -I. -DICE_CPP11_MAPPING -c client.cc Invoke.cpp
g++ -o client Invoke.o client.o -lIce++11

