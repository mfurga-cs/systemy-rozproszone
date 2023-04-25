#!/bin/bash

PROTOS_DIR=protos
PROTOS=protos/*.proto

JAVA_PLUGIN=./protoc-gen-grpc-java-1.54.0-linux-x86_64.exe
JAVA_OUT=./server/src/main/java

PYTHON_OUT=./client/

mkdir -p $JAVA_OUT
mkdir -p $PYTHON_OUT

python -m grpc_tools.protoc \
  -I$PROTOS_DIR \
  --python_out $PYTHON_OUT \
  --grpc_python_out $PYTHON_OUT \
  $PROTOS

protoc \
  -I$PROTOS_DIR \
  --plugin=protoc-gen-grpc-java=$JAVA_PLUGIN \
  --java_out=$JAVA_OUT \
  --grpc-java_out=$JAVA_OUT \
  $PROTOS

