# triton-server-learning

[Trition Inference Server](https://github.com/triton-inference-server/server) provided by NVIDIA, it provide good example and reference for GPU coding, Tensorrt building.


This repo is used to record my understanding and questions when reading the source code.


## To do inference with CURL for triton-inference-server url: v2/models/<model_name>/infer

* prepend image file size 1005970 in 4 bytes
```
printf "\x00\x0f\x59\x92" | cat - ./images/mug.jpg > stuff_mug
```
* prepare postdata json format, and append `stuff_mug` to it:
```
# cat postdata.json
{"inputs":[{"name":"INPUT","shape":[1,1],"datatype":"BYTES","parameters":{"binary_data_size":<size of file stuff_mug>}}],"outputs":[{"name":"OUTPUT","parameters":{"classification":3,"binary_data":true}}]}

# cat stuff_mug >> postdata.json
```
* do inference
```
# curl -X POST -H "Content-Type: application/octet-stream" -H "Inference-Header-Content-Length: <sizeof original postdata.json>" -H "Content-Length: <size of final postdata.json>" -H "Accept: */*" localhost:8000/v2/models/<model_name>/infer --data-binary "@postdata.json" -vv -o /workspace/myoutput
# cat /workspace/myoutput
{"model_name":"<model_name>","model_version":"1","outputs":[{"name":"OUTPUT","datatype":"BYTES","shape":[1,3],"parameters":{"binary_data_size":72}}]}0.723992:504:COFFEE MUG0.270952:968:CUP0.001160:967:ESPRESSO#
```
