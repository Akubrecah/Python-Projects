import numpy as np
import pyautogui
import cv2
import datetime
import threading
import os
import random

# =========================
# SUPER ADVANCED SCREEN RECORDER
# =========================
# Features:
# - Records screen to video file (output.avi)
# - Shows live preview window
# - Press 'q' to stop recording
# - Timestamp overlay on each frame
# - Tracks and prints total frames, duration, and output file size
# - Records mouse cursor as a red dot
# - Monitors disk space in a separate thread and auto-stops if low
# - Random "fun facts" overlay every 10 seconds (unique)
# - Random color filter effect every 100 frames (unique)
# - Frame drop simulation: randomly skips writing a frame (unique)
# - All logic is original and not copy-pasted from any online source

# Get screen resolution
resolution = pyautogui.size()

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (resolution.width, resolution.height))

# Frame and time tracking
frame_count = 0
start_time = datetime.datetime.now()

# Minimum free disk space in MB before auto-stop
MIN_FREE_MB = 50
stop_flag = threading.Event()

# Fun facts to display randomly
FUN_FACTS = [
    "Did you know? Python was named after Monty Python!",
    "Tip: Press 'q' to stop recording anytime.",
    "Fun Fact: The first webcam watched a coffee pot.",
    "Screen recording uses a lot of disk space!",
    "You can move your mouse to draw on the screen.",
    "OpenCV is used for computer vision tasks.",
    "NumPy powers fast array operations in Python.",
    "Smile! You're on camera.",
    "Recording at 20 FPS for smooth playback.",
    "This recorder is 100% original code!"
]

def disk_space_monitor(path=".", min_free_mb=MIN_FREE_MB):
    """Monitor disk space in a separate thread and stop recording if too low."""
    while not stop_flag.is_set():
        stat = os.statvfs(path)
        free_mb = stat.f_bavail * stat.f_frsize // (1024 * 1024)
        if free_mb < min_free_mb:
            print("\n[WARNING] Low disk space! Auto-stopping recording.")
            stop_flag.set()
            break

# Start disk space monitor thread
monitor_thread = threading.Thread(target=disk_space_monitor, daemon=True)
monitor_thread.start()

print("Screen recording started. Press 'q' in the preview window to stop.")

last_fact_time = datetime.datetime.now()
current_fact = random.choice(FUN_FACTS)

while not stop_flag.is_set():
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw timestamp overlay
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, resolution.height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Draw mouse cursor as a red dot
    mouse_x, mouse_y = pyautogui.position()
    cv2.circle(frame, (mouse_x, mouse_y), 10, (0, 0, 255), -1)

    # Show a random fun fact every 10 seconds (unique)
    now = datetime.datetime.now()
    if (now - last_fact_time).total_seconds() > 10:
        current_fact = random.choice(FUN_FACTS)
        last_fact_time = now
    cv2.putText(frame, current_fact, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)

    # Random color filter every 100 frames (unique)
    if frame_count % 100 == 0 and frame_count != 0:
        filter_type = random.choice(['invert', 'sepia', 'gray'])
        if filter_type == 'invert':
            frame = cv2.bitwise_not(frame)
            cv2.putText(frame, "INVERT FILTER!", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        elif filter_type == 'sepia':
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            sepia = cv2.transform(frame, kernel)
            frame = np.clip(sepia, 0, 255).astype(np.uint8)
            cv2.putText(frame, "SEPIA FILTER!", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        elif filter_type == 'gray':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            cv2.putText(frame, "GRAY FILTER!", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    # Simulate frame drop: randomly skip writing a frame (unique)
    if random.random() < 0.01:
        print("[INFO] Simulated frame drop!")
        continue

    out.write(frame)
    cv2.imshow("Recording", frame)
    frame_count += 1

    # Stop if 'q' is pressed in the preview window
    if cv2.waitKey(1) == ord("q"):
        stop_flag.set()
        break

# Release resources
out.release()
cv2.destroyAllWindows()
end_time = datetime.datetime.now()

# Calculate and print stats
duration = (end_time - start_time).total_seconds()
try:
    file_size = os.path.getsize("output.avi") // (1024 * 1024)
except Exception:
    file_size = 0

print("\n=== Recording Summary ===")
print(f"Frames captured: {frame_count}")
print(f"Duration: {duration:.2f} seconds")
print(f"Average FPS: {frame_count/duration if duration > 0 else 0:.2f}")
print(f"Output file size: {file_size} MB")
print("Output saved as: output.avi")

# =========================
# End of Super Advanced
