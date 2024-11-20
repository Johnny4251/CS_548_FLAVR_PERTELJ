import os
import cv2

def get_frame_data(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_cnt =  cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    time = frame_cnt / fps
    return frame_cnt, fps, time


def compute_vfi_video(video_path, new_name, model_pth="model/FLAVR_2x.pth", interpolation=2, slow_motion=True):
    if interpolation != 2 and interpolation != 4 and interpolation != 8:
        raise Exception("Interpolation level not supported")
    
    # raise exceptions if paths are not found
    if os.path.exists(video_path) == False: raise Exception("ERROR: Can not find video from path.")
    if os.path.exists(model_pth) == False: raise Exception("ERROR: Can not find model from path.")

    orig_cnt, orig_fps, orig_time = get_frame_data(video_path)

    # if not in slow_motion => use a higher res video instead by multiplying fps by interpolation factor
    if slow_motion == True:
        fps = int(orig_fps)
        os.system(f"python interpolate.py --input_video {video_path} --factor {interpolation} --load_model {model_pth} --output_fps {fps}")
    else:
        fps = int(orig_fps * interpolation)
        os.system(f"python interpolate.py --input_video {video_path} --factor {interpolation} --load_model {model_pth} --output_fps {fps}")


def main():
    compute_vfi_video("noice.mp4", "new_noice", "model/FLAVR_2x.pth", interpolation=2, slow_motion=False)


if __name__ == "__main__":
    main()