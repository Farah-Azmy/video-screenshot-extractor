import os
import cv2
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def extract_screenshots(input_folder, output_folder, log_widget):
    video_files = glob.glob(os.path.join(input_folder, '**', '*.mp4'), recursive=True)

    if not video_files:
        log_widget.insert(tk.END, "No .mp4 videos found.\n")
        return

    log_widget.insert(tk.END, f"🎥 Found {len(video_files)} video(s)\n")

    for video_path in video_files:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            log_widget.insert(tk.END, f"Could not open: {video_path}\n")
            continue

        relative_path = os.path.relpath(video_path, input_folder)
        path_parts = relative_path.split(os.sep)
        folder_name = path_parts[0] if len(path_parts) >= 2 else "unknown"
        save_folder = os.path.join(output_folder, folder_name)
        os.makedirs(save_folder, exist_ok=True)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_positions = [0, total_frames // 2, total_frames - 1]

        for idx, frame_pos in enumerate(frame_positions):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            ret, frame = cap.read()
            if ret:
                image_filename = f"image{idx + 1}.png"
                image_path = os.path.join(save_folder, image_filename)
                cv2.imwrite(image_path, frame)
                log_widget.insert(tk.END, f"Saved: {image_path}\n")
            else:
                log_widget.insert(tk.END, f"Failed to capture frame from {video_path}\n")
        cap.release()

def browse_input():
    folder = filedialog.askdirectory()
    input_var.set(folder)

def browse_output():
    folder = filedialog.askdirectory()
    output_var.set(folder)

def start_processing():
    input_folder = input_var.get()
    output_folder = output_var.get()

    if not os.path.isdir(input_folder) or not os.path.isdir(output_folder):
        messagebox.showerror("Invalid Folder", "Please select valid input and output folders.")
        return

    log_box.delete('1.0', tk.END)
    extract_screenshots(input_folder, output_folder, log_box)

# GUI Setup
root = tk.Tk()
root.title("Video Screenshot Extractor")
root.geometry("700x500")

input_var = tk.StringVar()
output_var = tk.StringVar()

tk.Label(root, text="Input Folder (Videos):").pack(pady=5)
tk.Entry(root, textvariable=input_var, width=70).pack()
tk.Button(root, text="Browse", command=browse_input).pack(pady=5)

tk.Label(root, text="Output Folder (Screenshots):").pack(pady=5)
tk.Entry(root, textvariable=output_var, width=70).pack()
tk.Button(root, text="Browse", command=browse_output).pack(pady=5)

tk.Button(root, text="Start Processing", command=start_processing, bg="green", fg="white").pack(pady=10)

log_box = scrolledtext.ScrolledText(root, height=15, width=80)
log_box.pack(pady=10)

root.mainloop()
