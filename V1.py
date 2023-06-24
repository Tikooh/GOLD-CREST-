
#https://pytorch.org/tutorials/intermediate/realtime_rpi.html All code is taken/modified from here

import time
import torch
import numpy as np
from torchvision import models, transforms #https://pytorch.org/vision/stable/transforms.html

import cv2
from PIL import Image

"""
https://pytorch.org/docs/stable/quantization.html
Quantization means to execute tensors with reduced precision to allows for a more compact model
Post Training dynamic quantization: weights are loaded from memory
"""

new_model = torch.ao.quantization.quantize_dynamic(
    original_model,
    {torch.nn.Linear} # layers to quantize
    dtype = torch.qint8 #data type, represents the target for quantized weights
)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, SPECIFY WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SPECIFY HEIGHT)
cap.set(cv2.CAP_PROP_FPS, 36)

#image Preprocessing
"""
Used to transform frames into format that the model can use.
"""

preprocess = transforms.Compose([

    transforms.ToTensor() #converts frame to a CHW torch tensor

    transforms.Normalize() #ensures that the data is in the same range as the activation function and allows less frequent non-zero gradients.
])


"""
Normalization is the fact of modifying the data of each channel/tensor so that the mean is zero and the standard deviation is one.
https://inside-machinelearning.com/en/why-and-how-to-normalize-data-object-detection-on-image-in-pytorch-part-1/
"""

with torch.no_grad(): #reduces memory usage, deactivates autograd
    



input_tensor = preprocess(image)



