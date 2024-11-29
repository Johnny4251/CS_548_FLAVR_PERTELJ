import os
import cv2
from pathlib import Path
import numpy as np

def get_video_data(video_path):
    capture = cv2.VideoCapture(video_path)
    frame_cnt =  capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = capture.get(cv2.CAP_PROP_FPS)
    if fps != 0: time = frame_cnt / fps
    else: time = 0
    return frame_cnt, fps, time

def play_video_from_path(video_path):
    _,fps,_ = get_video_data(video_path)
    fps = int(fps)

    cv2.namedWindow(video_path)
    capture = cv2.VideoCapture(video_path)

    if os.path.exists(video_path) == False: raise Exception("ERROR: Can not find video from path.")
    if not capture.isOpened(): raise Exception("ERROR: Could not open or find the video.")

    key = -1
    while key == -1:
        ret, frame = capture.read()
        if ret == True: cv2.imshow(video_path, frame)
        else: break
        key = cv2.waitKey(fps)

    capture.release()
    cv2.destroyAllWindows()

def play_video_from_list(video_list, fps, loop=False):
    fps = int(fps)

    cv2.namedWindow(f"Video {fps}")

    i=0
    while True:
        frame = video_list[i]
        cv2.imshow(f"Video {fps}", frame)
        key = cv2.waitKey(fps)
        if key == 27: break
        i += 1
        if (i > len(video_list)-1 and loop):
            i = 0
        elif (i > len(video_list)-1 and loop==False):
            break

    cv2.destroyAllWindows()

def play_comparison_videos(video1,video2, fps=-1):

    sub_images = []

    video1_window = "Video 1"
    video2_window = "Video 2"
    video3_window = "Subtracted Video"
    cv2.namedWindow(video1_window)
    cv2.namedWindow(video2_window)
    cv2.namedWindow(video3_window)

    # use the video w/ the least amount of frames
    # to avoid special errors
    video_len = min(len(video1), len(video2))
    for i in range(video_len):
        frame1 = video1[i]
        frame2 = video2[i]
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) 
        frame1_gray = frame1_gray.astype(np.float64) / 255.0
        frame2_gray = frame2_gray.astype(np.float64) / 255.0

        frame3 = np.absolute(frame1_gray - frame2_gray)
        sub_images.append(frame3)

        cv2.imshow(video1_window, frame1)
        cv2.imshow(video2_window, frame2)
        cv2.imshow(video3_window, frame3)
        
        cv2.waitKey(fps)

    cv2.destroyAllWindows()

    return sub_images

def get_video_frames(video_path):

    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened(): raise Exception("ERROR: Could not open or find the video.")
    
    video_frames = []
    while True:
        ret, frame = capture.read()
        if ret: video_frames.append(frame)
        else:
            capture.release()
            return video_frames

def compute_vfi_video(video_path, output_name, model_pth="model/FLAVR_2x.pth", interpolation=2, slow_motion=True):
    if interpolation != 2 and interpolation != 4 and interpolation != 8:
        raise Exception("Interpolation level not supported")
    
    # raise exceptions if paths are not found
    if os.path.exists(video_path) == False: raise Exception("ERROR: Can not find video from path.")
    if os.path.exists(model_pth) == False: raise Exception("ERROR: Can not find model from path.")

    _, orig_fps, _ = get_video_data(video_path)
    fps = int(orig_fps)

    # if not in slow_motion => use a higher res video instead by multiplying fps by interpolation factor
    if slow_motion == True:
        os.system(f"python interpolate.py --input_video {video_path} --factor {interpolation} --load_model {model_pth} --output_fps {fps}")
    else:
        fps *= int(interpolation)
        os.system(f"python interpolate.py --input_video {video_path} --factor {interpolation} --load_model {model_pth} --output_fps {fps}")

    try:
        new_path = Path(video_path).stem
        new_path += f".avi_{interpolation}x.avi"

        if not output_name.endswith(".avi"):
            output_name += ".avi"

        if os.path.exists(output_name):
            remove_flag = input(f"File: {output_name} already exists. Remove? (y/n): ")
            if remove_flag.lower().startswith("y"):
                os.remove(output_name)
            else:
                base_name = Path(output_name).stem
                output_name = f"{base_name}_NEW.avi"
                print(f"Output name changed to: {output_name}")

        os.rename(new_path, output_name)
    except Exception as e:
        print(f"Error during file renaming: {e}")
        output_name = video_path  # Fall back to original video path
    
    print(f"VFI VIDEO SAVED AS: {output_name}")
    return output_name, fps

    try:
        new_path = new_path[-4]
        new_path += f"_{interpolation}x.avi"
        output_name = output_name+".avi"
        if os.path.exists(output_name) == True: 
            remove_flag = input(f"File: {output_name} already exists. Remove? ")
            if remove_flag.lower()[0] == "y":
                os.remove(output_name)
            else:
                output_name = Path(output_name).stem
                output_name += "(NEW).avi"
        os.rename(new_path, output_name)
    except Exception as e:
        print(e)
        output_name = video_path
    
    print(f"VFI VIDEO SAVED AS: {output_name}")
    return output_name, fps

def compare_videos(video, ground, interpolation=2):
    if interpolation > 0:
        video_path, _ = compute_vfi_video(video, f"new_{video}_{interpolation}x", f"model/FLAVR_{interpolation}x.pth", interpolation=interpolation, slow_motion=True)
    else: video_path = video
    video_frames = get_video_frames(video_path)
    ground_frames = get_video_frames(ground)
    diff_video = play_comparison_videos(video_frames,ground_frames)
    return diff_video

def main():
    videos_to_interpolate = ['punch_original.mp4', 'sprite_original.mp4', 'sheep_25fps.mp4']
    for video in videos_to_interpolate:
        if os.path.exists(video) == False: 
            print("Can not find video.. skipping")
            continue
        print(f"Interpolating: {video}")
        interp = 2
        max_interp = 8
        while interp <= max_interp:
            new_name = f"new_{video}_{interp}x"
            video_path, fps = compute_vfi_video(video, new_name, f"model/FLAVR_{interp}x.pth", interpolation=interp, slow_motion=True)
            print(video_path, fps)
            #play_video_from_path(video_path)
            interp = interp << 1 # multiply by 2

if __name__ == "__main__":
    main() 