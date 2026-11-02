import cv2
import numpy as np

def detect_static_regions(frame1, frame2, threshold=30):
    """Detect static regions by comparing difference between two frames."""
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    static_mask = cv2.dilate(thresh, None, iterations=2)
    return static_mask

def check_static_regions(input_video):
    print("Checking static regions...")
    cap = cv2.VideoCapture(input_video)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames != 315:
        print(f"Error: Video has {total_frames} frames, expected 315 frames.")
        cap.release()
        return None

    prev_frame = None
    static_frames = 0
    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Cannot read frame {i+1}")
            cap.release()
            return None
        if prev_frame is not None:
            static_mask = detect_static_regions(prev_frame, frame)
            if np.sum(static_mask) > 0:
                static_frames += 1
        prev_frame = frame.copy()
    cap.release()

    print(f"Number of static frames: {static_frames}")
    if static_frames >= 84:  # Assuming 84 bits needed for "trung2"
        print("Step 2C completed: Video has enough static frames.")
        with open("static_frames.txt", "w") as f:
            f.write(str(static_frames))
            print("File static_frames.txt created successfully.")  # Thêm thông điệp xác nhận file
        return static_frames
    else:
        print("Step 2C failed: Not enough static frames.")
        return None

if __name__ == "__main__":
    input_video = "input.mp4"
    static_frames = check_static_regions(input_video)
    if static_frames is not None:
        print("Static region check successful.")
    else:
        print("Static region check failed.")
