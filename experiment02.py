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

def compute_mse(subtracted_video):
    errors = []
    for frame in subtracted_video:
        frame = np.array(frame)
        frame_error = np.mean(frame**2)
        errors.append(frame_error)
    
    return np.mean(errors)

def save_sub_video(sub_images, fps, output_file):
    if not sub_images:
        raise ValueError("The sub_images list is empty.")

    height, width = sub_images[0].shape
    for idx, image in enumerate(sub_images):
        if image.shape != (height, width):
            raise ValueError(f"Frame {idx} has inconsistent dimensions: {image.shape}. Expected: ({height}, {width}).")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), isColor=False)

    for idx, image in enumerate(sub_images):
        if not np.issubdtype(image.dtype, np.floating):
            raise ValueError(f"Frame {idx} is not a valid floating-point grayscale image.")
        if image.min() < 0 or image.max() > 1:
            raise ValueError(f"Frame {idx} values are out of range [0, 1].")
        frame = (image * 255).astype(np.uint8)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        out.write(frame_bgr)

    out.release()

    print(f"Subtracted video saved successfully to {output_file}.")

def chop_frame_comparison(video, skip_count=2):
    _,fps,_ = get_video_data(video)
    new_fps = fps // skip_count
    video_frames = get_video_frames(video_path=video)
    discarded_video = discard_frames(video_frames, skip_count)
    play_video_from_list(discarded_video, new_fps, loop=True)
    discarded_video_path = save_video_from_list(discarded_video, new_fps,f"discarded_video_{skip_count}.avi")
    print("chopped video..")

    output_path = f"{video}_{skip_count}"
    output_path,output_fps = compute_vfi_video(discarded_video_path, output_path, f"model/FLAVR_{skip_count}x.pth", interpolation=skip_count, slow_motion=False)
    video1 = scale_video_list(get_video_frames(video))
    video2 = scale_video_list(get_video_frames(output_path))
    #play_video_from_list(video1, fps, loop=True)
    sub_images = play_comparison_videos(video1, video2, fps=output_fps)
    error = compute_mse(sub_images)

    round_val = 6
    print(f"SKIP COUNT:\t{skip_count}\nOLD FPS:\t{fps}\nNEW FPS:\t{new_fps}")
    print(f"Mean Squared Error:\t{np.round(error, round_val)}")
    play_video_from_list(sub_images, fps, loop=True)

def main():
    chop_frame_comparison("bird.mp4", skip_count=8)

if __name__ == "__main__":
    main()