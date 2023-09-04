import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys, pathlib
from detect import Detector

root = pathlib.Path()
detector = Detector(model=root/'models'/'best.pt',names=root/'data.yaml', stream=False, video = "actual_turret_video.mp4", edge=False)

for i in range(100):
    if i < 10:
        pass
    frame = detector.getNextFrame()
    x = detector.detectFrame(frame, draw_img=False)