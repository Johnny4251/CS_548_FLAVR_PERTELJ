import os
import cv2

def get_frame_data(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_cnt =  cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    time = frame_cnt / fps
    return frame_cnt, fps, time

def compute_vfi_video(video_path, output_name, model_pth="model/FLAVR_2x.pth", interpolation=2, slow_motion=True):
    if interpolation != 2 and interpolation != 4 and interpolation != 8:
        raise Exception("Interpolation level not supported")
    
    # raise exceptions if paths are not found
    if os.path.exists(video_path) == False: raise Exception("ERROR: Can not find video from path.")
    if os.path.exists(model_pth) == False: raise Exception("ERROR: Can not find model from path.")

    orig_cnt, orig_fps, orig_time = get_frame_data(video_path)
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
    vfi_info = compute_vfi_video("noice.mp4", "new_noice", f"model/FLAVR_{interp}x.pth", interpolation=interp, slow_motion=True)
    print(vfi_info)


if __name__ == "__main__":
    main()