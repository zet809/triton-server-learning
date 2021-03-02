# This file show the basic steps to read an image and generate a non-binary json file for model in triton

import cv2, json
import numpy as np

data=cv2.imread("./images/mug.jpg").astype(np.float32)
data=cv2.resize(data, (224,224), cv2.INTER_AREA)
data = data[:,:,::-1].transpose((2,0,1))
data /= 255.0
mylist=data.reshape([3*224*224])


 myjson={"inputs":[{"name":"gpu_0/data", "shape":[1,3,224,224],"datatype":"FP32", "data":mylist.tolist()}], 
         "outputs":[{"name":"gpu_0/softmax","parameters":{"classification":3,"binary_data":True}}]}

with open("./mypostdata.json", 'w') as f:
    f.write(json.dumps(myjson))
