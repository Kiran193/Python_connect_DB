# This config is tuned for the bundle of person-detection-retail-xxx and person-reidentification-retail-xxx
# models, but should be suitable for other well-trained detector and reid models
# Alse all tracking update intervals are set assumin input frequency about 30FPS
import os 
import sys
from datetime import datetime


time_window = 20
global_match_thresh = 0.35

sct_config = dict(
    time_window=10,
    continue_time_thresh=2,
    track_clear_thresh=3000,
    match_threshold=0.475,
    merge_thresh=0.3,
    n_clusters=4,
    max_bbox_velocity=0.2,
    detection_occlusion_thresh=0.7,
    track_detection_iou_thresh=0.5
)

#Model files. TODO: Change from static to dynamic paths.
person_detect_model = "counter\\models\\person-detection-retail-0013.xml"
person_reid_model = "counter\\models\\person-reidentification-retail-0200.xml"
face_det_model="counter\\models\\face-detection-retail-0005.xml"
face_weights="counter\\models\\face-detection-retail-0005.bin"
mask_det_model="counter\\face_detector_mask\\mask_detector.model"

threshold_person_detection = 0.80
faceconfidence_mask = 0.90
device = "CPU"
cpu_extension = None # (MKLDNN (CPU)-targeted custom layers. Absolute path to a shared library with the kernels impl.', type=str)
enter_to_db = True
save_video=True
output_video_path="D:\\Work\\counter-electron-app\\"

show_video=True
demo_video_feed=['D:\\Work\\counter-electron-app\\normal_entry.mp4']
# demo_video_feed=['rtsp://admin:kayathebird!@192.168.1.64:554/H.264']



#store details
dummy_store_details={'store_name': 'DummyStore1', 'store_location':'Bangalore', 'geo_location':[0,0], 'created_at':datetime.now()}