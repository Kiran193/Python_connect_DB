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


threshold_person_detection = 0.80
faceconfidence_mask = 0.90
device = "CPU"
cpu_extension = None # (MKLDNN (CPU)-targeted custom layers. Absolute path to a shared library with the kernels impl.', type=str)
enter_to_db = True
save_video=True

show_video=True


#store details
dummy_store_details={'store_name': 'DummyStore1', 'store_location':'Bangalore', 'geo_location':[0,0], 'created_at':datetime.now()}
