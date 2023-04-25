#!/bin/bash

mkdir stub
slice2cpp --output-dir stub Invoke.ice
g++ -Istub -DICE_CPP11_MAPPING -c client.cc stub/Invoke.cpp
g++ -o client Invoke.o client.o -lIce++11

