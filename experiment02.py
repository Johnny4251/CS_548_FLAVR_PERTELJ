import experiment01
from experiment01 import *

# This takes in a list of videos and discards
# every x frame. Then returns the new video as a list.
def discard_frames(frames, skip_rate=2):
    if len(frames) <= skip_rate: raise Exception("Error: Empty frames.")
    
    new_frames = []
    for i in range(0, len(frames)-1, skip_rate):
        new_frames.append(frames[i])
    
    return new_frames

def save_video_from_list(video_list, fps, output_path="output_video.avi"):

    if not video_list: raise Exception("ERROR: Cannot save an empty video.")
    
    height, width, channels = video_list[0].shape
    if channels != 3:raise Exception("Frames must have 3 channels.")
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in video_list: writer.write(frame)
    writer.release()
    print(f"Video saved as: {output_path}")
    return output_path

def scale_video_list(video_list, fx=0.5, fy=0.5):
    new_video_list = []
    for i in range(len(video_list)):
        new_video_list.append(cv2.resize(video_list[i], None, fx=fx, fy=fy))
    return new_video_list

def main():
    video = "punch_original.mp4"
    _,fps,_ = experiment01.get_video_data(video)
    skip_count = 2
    new_fps = fps // skip_count
    print(f"SKIP COUNT:\t{skip_count}\nOLD FPS:\t{fps}\nNEW FPS:\t{new_fps}")
    video_frames = experiment01.get_video_frames(video_path=video)
    discarded_video = discard_frames(video_frames, skip_count)
    experiment01.play_video_from_list(discarded_video, new_fps, loop=True)
    discarded_video_path = save_video_from_list(discarded_video, new_fps,f"discarded_video_{skip_count}.avi")

    output_path = f"{video}_{skip_count}"
    #output_path,output_fps = experiment01.compute_vfi_video(discarded_video_path, output_path, f"model/FLAVR_{skip_count}x.pth", interpolation=skip_count, slow_motion=False)
    #output_path = f"punch_original.mp4_{skip_count}.avi"
    #output_fps = 30
    print(output_path)
    
    video1 = scale_video_list(get_video_frames(video))
    video2 = scale_video_list(get_video_frames(output_path))
    #experiment01.play_video_from_list(video1, fps, loop=True)
    sub_images = experiment01.play_comparison_videos(video1, video2, fps=output_fps)
    experiment01.play_video_from_list(sub_images, fps, loop=True)

if __name__ == "__main__":
    main()