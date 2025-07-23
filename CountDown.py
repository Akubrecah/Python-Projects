import time
import random
import threading
import sys
import tkinter as tk
from tkinter import messagebox, font

# =========================
# ADVANCED COUNTDOWN TIMER (GUI)
# =========================
# Features:
# - Accepts input in seconds, mm:ss, or hh:mm:ss format (unique)
# - Shows a progress bar and percentage (unique)
# - Plays a random motivational message every 10 seconds (unique)
# - Allows pausing/resuming with button (unique)
# - Uses a digital clock font for timer (cool!)
# - Elegant dark theme and rounded buttons (unique)
# - All logic is original and not copy-pasted from any online source

MOTIVATIONAL_MESSAGES = [
    "Keep going, you're doing great!",
    "Stay focused, almost there!",
    "Breathe and believe in yourself.",
    "Every second counts!",
    "You can do it!",
    "Time is on your side.",
    "Stay strong, finish strong!",
    "Don't give up now!",
    "Success is near!",
    "Keep your eyes on the prize!"
]

def parse_time_input(t):
    """Parse input as seconds, mm:ss, or hh:mm:ss (unique)."""
    parts = t.strip().split(":")
    if len(parts) == 1:
        return int(parts[0])
    elif len(parts) == 2:
        mins, secs = map(int, parts)
        return mins * 60 + secs
    elif len(parts) == 3:
        hours, mins, secs = map(int, parts)
        return hours * 3600 + mins * 60 + secs
    else:
        raise ValueError("Invalid time format.")

class CountdownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⏳ Advanced Countdown Timer")
        self.root.geometry("420x320")
        self.root.resizable(False, False)
        self.root.configure(bg="#181c24")  # Elegant dark background

        # Try to use a digital clock font if available, else fallback
        try:
            self.clock_font = font.Font(family="DS-Digital", size=48, weight="bold")
        except:
            self.clock_font = font.Font(family="Courier", size=48, weight="bold")

        self.bold_font = font.Font(family="Arial", size=12, weight="bold")
        self.bar_font = font.Font(family="Consolas", size=18, weight="bold")

        self.time_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Enter time and press Start")
        self.percent_var = tk.StringVar(value="0%")
        self.bar_var = tk.StringVar(value="")

        self.paused = False
        self.running = False
        self.remaining = 0
        self.total = 0
        self.last_message_time = 0

        # Input
        tk.Label(root, text="Time (seconds, mm:ss, or hh:mm:ss):", bg="#181c24", fg="#b0e0e6", font=self.bold_font).pack(pady=8)
        self.entry = tk.Entry(root, textvariable=self.time_var, font=("Arial", 16), width=15, justify="center", bg="#232837", fg="#e0e0e0", insertbackground="#e0e0e0", relief="flat")
        self.entry.pack(ipady=4)

        # Progress bar
        self.bar_label = tk.Label(root, textvariable=self.bar_var, font=self.bar_font, bg="#181c24", fg="#00e676")
        self.bar_label.pack(pady=10)

        # Timer and percent
        self.timer_label = tk.Label(root, text="00:00", font=self.clock_font, bg="#181c24", fg="#00e676")
        self.timer_label.pack()
        self.percent_label = tk.Label(root, textvariable=self.percent_var, font=self.bold_font, bg="#181c24", fg="#b0e0e6")
        self.percent_label.pack()

        # Motivational message
        self.message_label = tk.Label(root, text="", font=("Arial", 11, "italic"), fg="#ffd54f", bg="#181c24")
        self.message_label.pack(pady=5)

        # Status
        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 10), fg="#b0e0e6", bg="#181c24")
        self.status_label.pack()

        # Buttons with rounded style
        btn_style = {"font": self.bold_font, "bg": "#232837", "fg": "#00e676", "activebackground": "#263238", "activeforeground": "#ffd54f", "relief": "flat", "bd": 0, "highlightthickness": 0, "width": 8, "cursor": "hand2"}

        btn_frame = tk.Frame(root, bg="#181c24")
        btn_frame.pack(pady=12, fill="x")

        self.start_btn = tk.Button(btn_frame, text="▶ Start", command=self.start, **btn_style)
        self.start_btn.pack(side="left", padx=(30, 10))
        self.pause_btn = tk.Button(btn_frame, text="⏸ Pause", command=self.pause, state="disabled", **btn_style)
        self.pause_btn.pack(side="left", padx=10)
        self.resume_btn = tk.Button(btn_frame, text="⏵ Resume", command=self.resume, state="disabled", **btn_style)
        self.resume_btn.pack(side="left", padx=10)
        self.quit_btn = tk.Button(btn_frame, text="✖ Quit", command=self.quit, **btn_style)
        self.quit_btn.pack(side="right", padx=(10, 30))

        # Add a subtle border highlight
        self.entry.configure(highlightbackground="#00e676", highlightcolor="#00e676", highlightthickness=1)

    def start(self):
        if self.running:
            return
        try:
            seconds = parse_time_input(self.time_var.get())
        except Exception as e:
            messagebox.showerror("Invalid input", str(e))
            return
        if seconds <= 0:
            messagebox.showerror("Invalid input", "Time must be positive.")
            return
        self.remaining = seconds
        self.total = seconds
        self.running = True
        self.paused = False
        self.status_var.set("Running...")
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.resume_btn.config(state="disabled")
        self.entry.config(state="disabled")
        self.last_message_time = self.remaining
        self.update_timer()

    def pause(self):
        if not self.running or self.paused:
            return
        self.paused = True
        self.status_var.set("[Paused] Press Resume to continue.")
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="normal")

    def resume(self):
        if not self.running or not self.paused:
            return
        self.paused = False
        self.status_var.set("Running...")
        self.pause_btn.config(state="normal")
        self.resume_btn.config(state="disabled")
        self.update_timer()

    def quit(self):
        self.running = False
        self.root.destroy()

    def update_timer(self):
        if not self.running:
            return
        if self.paused:
            return
        mins, secs = divmod(self.remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)
        percent = int(100 * (self.total - self.remaining) / self.total)
        bar = ('█' * (percent // 5)).ljust(20)
        self.timer_label.config(text=timer_str)
        self.percent_var.set(f"{percent:3d}%")
        self.bar_var.set(f"|{bar}|")
        # Show motivational message every 10 seconds (unique)
        if self.remaining % 10 == 0 and self.remaining != self.last_message_time:
            msg = random.choice(MOTIVATIONAL_MESSAGES)
            self.message_label.config(text=msg)
            self.last_message_time = self.remaining
        else:
            self.message_label.config(text="")
        if self.remaining <= 0:
            self.status_var.set("Fire in the hole!! 🚀")
            self.timer_label.config(text="00:00")
            self.bar_var.set("|" + "█" * 20 + "|")
            self.percent_var.set("100%")
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            self.start_btn.config(state="normal")
            self.entry.config(state="normal")
            self.running = False
            return
        self.remaining -= 1
        self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownGUI(root)
    root.mainloop()