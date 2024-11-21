import os
import cv2

def get_video_data(video_path):
    capture = cv2.VideoCapture(video_path)
    frame_cnt =  capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = capture.get(cv2.CAP_PROP_FPS)
    time = frame_cnt / fps
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

def play_video_from_list(video_list, fps):
    fps = int(fps)

    cv2.namedWindow(f"Video {fps}")

    for i in range(len(video_list)):
        frame = video_list[i]
        cv2.imshow(f"Video {fps}", frame)
        key = cv2.waitKey(fps)
        if key == 27: break
    cv2.destroyAllWindows()

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
        # rename interpolated video to the output video + .avi extension
        new_path = video_path[:-4] + f"_{interpolation}x.avi"
        output_name = output_name+".avi"
        if os.path.exists(output_name) == True: 
            remove_flag = input(f"File: {output_name} already exists. Remove? ")
            if remove_flag.lower()[0] == "y":
                os.remove(output_name)
            else:
                output_name = output_name[:-4]
                output_name += "(NEW).avi"
        os.rename(new_path, output_name)
    except Exception as e:
        print(e)
        output_name = video_path
    
    print(f"VFI VIDEO SAVED AS: {output_name}")
    return output_name, fps

def main():
    interp = 8
    video_path,fps = compute_vfi_video("noice.mp4", f"new_noice_{interp}x", f"model/FLAVR_{interp}x.pth", interpolation=interp, slow_motion=True)
    print(video_path, fps)

    #play_video_from_path(video_path)
    video_frames = get_video_frames(video_path)
    play_video_from_list(video_frames, fps)

if __name__ == "__main__":
    main()