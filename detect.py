'''
From https://github.com/jveitchmichaelis/edgetpu-yolo/tree/main
created by jveitchmichaelis
modified by kolesniii
'''

import logging
import time

import numpy as np
from tqdm import tqdm
import cv2

from edgetpumodel import EdgeTPUModel
from utils import get_image_tensor

class Detector:
    def __init__(self, model: str, names : str, conf_thresh : float = 0.50, iou_thresh : float = 0.45, quiet: bool = False, 
                 device : int = 0, stream : bool = True, video : str= None) -> None:
        '''
        Detector class for running a Yolov5 model on an EdgeTPU
        Model : path to edgetpu-compiled tflite file
        Names : yaml names file (yolov5 format)
        Conf_thresh : detection threshold, float between 0 and 1
        Iou_thresh : NMS threshold, float between 0 and 1
        Quiet : disable logging, bool
        Device : device number for stream, int
        Stream : use stream instead of video, bool
        Video : path to video file, str
        '''
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        if quiet:
            logging.disable(logging.CRITICAL)
            self.logger.disabled = True
        
        self.model = EdgeTPUModel(model, names, conf_thresh=conf_thresh, iou_thresh=iou_thresh)
        self.input_size = self.model.get_image_size()
        x = (255*np.random.random((3,*self.input_size))).astype(np.uint8)
        self.model.forward(x)

        if stream and video is not None:
            self.logger.warning("Both stream and video specified, defaulting to video")
            stream = False #priority goes to video
        if stream:
            self.logger.info("Opening stream on device: {}".format(device))
            self.video = cv2.VideoCapture(device)
            self.video.set(cv2.CAP_PROP_FPS, 30)
            self.video.set(3,640)
            self.video.set(4,640)
        elif video is not None:
            self.logger.info("Opening video file: {}".format(video))
            self.video = cv2.VideoCapture(video)
            self.video.set(cv2.CAP_PROP_FPS, 30)
        else:
            self.logger.critical("No video or stream specified")
            raise IOError("No video or stream specified")

    def benchSpeed(self, iterations : int = 100) -> None:
        '''
        Benchmarks the speed of the model
        '''
        self.logger.info("Performing test run")
        
        inference_times = []
        nms_times = []
        total_times = []
        
        for i in tqdm(range(iterations)):
            x = (255*np.random.random((3,*self.input_size))).astype(np.float32)
            
            pred = self.model.forward(x)
            tinference, tnms = self.model.get_last_inference_time()
            
            inference_times.append(tinference)
            nms_times.append(tnms)
            total_times.append(tinference + tnms)
            
        inference_times = np.array(inference_times)
        nms_times = np.array(nms_times)
        total_times = np.array(total_times)
            
        self.logger.info("Inference time (EdgeTPU): {:1.2f} +- {:1.2f} ms".format(inference_times.mean()/1e-3, inference_times.std()/1e-3))
        self.logger.info("NMS time (CPU): {:1.2f} +- {:1.2f} ms".format(nms_times.mean()/1e-3, nms_times.std()/1e-3))
        fps = 1.0/total_times.mean()
        self.logger.info("Mean FPS: {:1.2f}".format(fps))

    def getNextFrame(self) -> np.ndarray:
        '''
        Returns next frame from input source
        '''
        res, image = self.video.read()
        return cv2.rotate(image, cv2.ROTATE_180)
    
    def getLastProcessingTime(self) -> float:
        '''
        Returns the last frame's processing time in seconds
        '''
        times = self.model.get_last_inference_time()
        return sum(times)
    
    def detectFrame(self, frame, draw_img=False, save_img=False, save_txt=False, output_path="detection.jpg", 
                    hide_labels=False, hide_conf=False) -> list[list[float, float, float, float, float]]:
        '''
        Detects objects in a frame, returns list of [top left x, top left y, bottom right x, bottom right y, confidence]
        Frame : cv2 image to detect objects in
        Draw_img : draw image in separate window, bool
        Save_img : save image, bool
        Save_txt : save txt file, bool
        Save_path : path to save image and txt file, str
        Hide_labels : hide labels on drawn image, bool
        Hide_conf : hide confidence on drawn image, bool
        '''
        full_image, net_image, pad = get_image_tensor(frame, self.model.get_image_size()[0])
        pred = self.model.forward(net_image)
        det = self.model.process_predictions(pred[0], full_image, pad, draw_img=draw_img, 
                                             save_img=save_img, save_txt=save_txt, output_path=output_path, 
                                             hide_labels=hide_labels, hide_conf=hide_conf)
        return det
    
    def test_input(self, timeout: float = 30) -> None:
        '''
        Tests input source by rendening frames for specified time
        Timeout : time to render frames in seconds, int or float
        '''
        self.logger.info("Testing input source for {} seconds".format(timeout))
        start = time.time()
        while time.time() - start < timeout:
            image = self.getNextFrame()
            cv2.imshow("image", image)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        self.logger.info("Test complete, windows closed")

    def destroy(self) -> None:
        '''
        Closes input source, destroys windows
        Renders class unusable
        '''
        self.video.release()
        cv2.destroyAllWindows()
        self.logger.warning("Input source closed, class destroyed")

            
        

    

