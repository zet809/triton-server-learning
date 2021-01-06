# triton-server-learning

[Trition Inference Server](https://github.com/triton-inference-server/server) provided by NVIDIA, it provide good example and reference for GPU coding, Tensorrt building.


This repo is used to record my understanding and questions when reading the source code.


## To do inference with CURL for triton-inference-server url: v2/models/<model_name>/infer

* prepend image file size 1005970(0x0f5992)
```
printf "\x00\x0f\x59\x92" | cat - ./images/mug.jpg > stuff_mug
```
* prepare postdata json format, and append image size and image data to it:
```
# cat postdata.json
{"inputs":[{"name":"INPUT","shape":[1,1],"datatype":"BYTES","parameters":{"binary_data_size":<size of file stuff_mug>}}],"outputs":[{"name":"OUTPUT","parameters":{"classification":3,"binary_data":true}}]}

# printf "\x00\x0f\x59\x92" | cat - ./images/mug.jpg >> postdata.json
# ls -l postdata.json
-rw-r--r-- 1 root root 1006161 Jan  6 05:50 postdata.json
```
* do inference
```
# curl -X POST -H "Content-Type: application/octet-stream" -H "Inference-Header-Content-Length: <sizeof original postdata.json>" -H "Content-Length: <size of final postdata.json, 1006161 here>" -H "Accept: */*" localhost:8000/v2/models/<model_name>/infer --data-binary "@postdata.json" -vv -o /workspace/myoutput
# cat /workspace/myoutput
{"model_name":"<model_name>","model_version":"1","outputs":[{"name":"OUTPUT","datatype":"BYTES","shape":[1,3],"parameters":{"binary_data_size":72}}]}0.723992:504:COFFEE MUG0.270952:968:CUP0.001160:967:ESPRESSO#
```
