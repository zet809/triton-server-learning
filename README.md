# triton-server-learning

[Trition Inference Server](https://github.com/triton-inference-server/server) provided by NVIDIA, it provide good example and reference for GPU coding, Tensorrt building.


This repo is used to record my understanding and questions when reading the source code.

## To load ensemble example models:

* start tritonserver build container (my build for r20.07)
```
# nvidia-docker  run -e NVIDIA_VISIBLE_DEVICES=0 --privileged -it -p8000:8000 -p8001:8001 -p8002:8002 -v $(pwd)/src:/workspace/src tritonserver_build:r20.07 bash
```

* download example models
```
# cd /workspace/docs/examples/
# ./fetch_models.sh
# mv model_repository/resnet50_netdef/1/ ensemble_model_repository/resnet50_netdef/
```
* get model file `libimagepreprocess.so` for image_preprocess_nchw_3x224x224_inception from https://github.com/triton-inference-server/server/releases/download/v1.15.0/v1.15.0_ubuntu1804.custombackend.tar.gz, and put it under ensemble_model_repository/image_preprocess_nchw_3x224x224_inception/1/
* install needed lib for `libimagepreprocess.so`
```
apt-get update && apt-get install libopencv-highgui-dev
```

* create version directory for ensemble model

* the working directory looks like this:
```
# tree ./ensemble_model_repository/
./ensemble_model_repository/
|-- image_preprocess_nchw_3x224x224_inception
|   |-- 1
|   |   `-- libimagepreprocess.so
|   `-- config.pbtxt
|-- preprocess_resnet50_ensemble
|   |-- 1
|   `-- config.pbtxt
`-- resnet50_netdef
    |-- 1
    |   |-- init_model.netdef
    |   `-- model.netdef
    |-- config.pbtxt
    `-- resnet50_labels.txt

6 directories, 7 files
```

* start triton server

```
# /opt/tritonserver/bin/tritonserver --model-repository=./ensemble_model_repository/
```
## To do inference with CURL for triton-inference-server url: v2/models/<model_name>/infer

* prepend image file size 1005970(0x0f5992)
```
# printf "\x00\x0f\x59\x92" | cat - ./images/mug.jpg > stuff_mug
# ls -l stuff_mug
-rw-r--r-- 1 root root 1005974 Feb  3 01:35 stuff_mug
```
* prepare postdata json format, and append image size and image data to it:
```
# cat postdata.json
{"inputs":[{"name":"INPUT","shape":[1,1],"datatype":"BYTES","parameters":{"binary_data_size":<size of file stuff_mug, 1005974 here>}}],"outputs":[{"name":"OUTPUT","parameters":{"classification":3,"binary_data":true}}]}
# ls -l postdata.json
-rw-r--r-- 1 root root 188 Feb  3 01:35 postdata.json
# printf "\x00\x0f\x59\x92" | cat - ./images/mug.jpg >> postdata.json
# ls -l postdata.json
-rw-r--r-- 1 root root 1006161 Jan  6 05:50 postdata.json
```
* do inference
```
# curl -X POST -H "Content-Type: application/octet-stream" -H "Inference-Header-Content-Length: <sizeof original postdata.json, 188 here>" -H "Content-Length: <size of final postdata.json, 1006161 here>" -H "Accept: */*" localhost:8000/v2/models/<model_name>/infer --data-binary "@postdata.json" -vv -o /workspace/myoutput
# cat /workspace/myoutput
{"model_name":"<model_name>","model_version":"1","outputs":[{"name":"OUTPUT","datatype":"BYTES","shape":[1,3],"parameters":{"binary_data_size":72}}]}0.723992:504:COFFEE MUG0.270952:968:CUP0.001160:967:ESPRESSO#
```
