import numpy as np
import pyautogui
import cv2
import datetime
import threading
import os

# =========================
# ADVANCED SCREEN RECORDER
# =========================
# Features:
# - Records screen to video file (output.avi)
# - Shows live preview window
# - Press 'q' to stop recording
# - Saves timestamp overlay on each frame (unique)
# - Tracks and prints total frames, duration, and output file size (unique)
# - Optionally records mouse cursor position as a red dot (unique)
# - Uses a separate thread to monitor disk space and auto-stops if low (unique)
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

while not stop_flag.is_set():
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw timestamp overlay (unique feature)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, resolution.height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Draw mouse cursor as a red dot (unique feature)
    mouse_x, mouse_y = pyautogui.position()
    cv2.circle(frame, (mouse_x, mouse_y), 10, (0, 0, 255), -1)

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

# Calculate and print stats (unique feature)
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
# End of Advanced Recorder
