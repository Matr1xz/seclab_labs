import cv2
import numpy as np

def string_to_bin(message):
    length = len(message)
    length_bin = format(length, '016b')  
    message_bin = ''.join(format(ord(c), '08b') for c in message)
    return length_bin + message_bin

def calculate_energy_difference(frame1_dct, frame2_dct):
    return np.sum(np.abs(frame1_dct - frame2_dct))

def hide_message_in_frame(frame, message_bin, message_index, prev_dct, threshold=0.5):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dct_frame = cv2.dct(np.float32(gray_frame))

    if prev_dct is not None:
        energy_diff = calculate_energy_difference(prev_dct, dct_frame)
    else:
        energy_diff = 0

    modified_frame = cv2.idct(dct_frame)
    return np.uint8(modified_frame), message_index, dct_frame

def embed_message_in_video(input_video_path, output_video_path, secret_message, threshold=0.5):
    cap = None
    out = None
    message_bin = string_to_bin(secret_message)
    message_index = 0
    prev_dct = None

    try:
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video: {input_video_path}")
            return

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height), isColor=False)
        if not out.isOpened():
            print(f"Error: Cannot create VideoWriter at {output_video_path}.")
            return

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            modified_frame, message_index, prev_dct = hide_message_in_frame(
                frame, message_bin, message_index, prev_dct, threshold)

            out.write(modified_frame)
            print(f"Frame {frame_count}/{total_frames} processed. Embedded bits: {message_index}/{len(message_bin)}")

        print(f"Total embedded bits: {message_index}/{len(message_bin)}")
        if message_index < len(message_bin):
            print("Warning: Not all message bits were embedded.")

    finally:
        if cap:
            cap.release()
        if out:
            out.release()

input_file_path = 'input_text.txt'
with open(input_file_path, 'r') as file:
    secret_message = file.read()

input_video_file = 'sample_video.mpeg'
output_video_file = 'stego_video_energy.avi'
threshold = 0.5

embed_message_in_video(input_video_file, output_video_file, secret_message, threshold)
print("\n DCT-based embedding completed.")

