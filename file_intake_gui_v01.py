import json
import re
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog


OUTPUT_DIR = "gui_preview_output"


def normalize_folder_path(raw_path: str) -> str:
    path = raw_path.strip()

    windows_match = re.match(r"^([A-Za-z]):\\", path)
    if windows_match:
        drive_letter = windows_match.group(1).lower()
        rest = path[2:].replace("\\", "/")
        return f"/mnt/{drive_letter}{rest}"

    return path


def choose_folder(folder_var: tk.StringVar,
                  status_var: tk.StringVar,
                  summary_var: tk.StringVar) -> None:
    folder = filedialog.askdirectory(title="Choose folder")
    if not folder:
        return

    folder_var.set(folder)
    status_var.set("Status: Folder selected")
    summary_var.set("No preview yet")


def run_preview(folder_var: tk.StringVar,
                status_var: tk.StringVar,
                summary_var: tk.StringVar) -> None:
    raw_folder = folder_var.get().strip()

    if not raw_folder:
        status_var.set("Status: No folder selected")
        return

    folder = normalize_folder_path(raw_folder)
    folder_var.set(folder)

    folder_path = Path(folder)
    if not folder_path.exists() or not folder_path.is_dir():
        status_var.set("Status: Folder path is not valid")
        summary_var.set("No preview yet")
        return

    try:
        subprocess.run(
            [
                "python3",
                "file_intake_assistant_v1.py",
                "--root",
                folder,
                "--output-dir",
                OUTPUT_DIR,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        summary_path = Path(OUTPUT_DIR) / "summary.json"
        if not summary_path.exists():
            status_var.set("Status: Preview created, but summary not found")
            summary_var.set("No preview yet")
            return

        with summary_path.open("r", encoding="utf-8") as f:
            summary = json.load(f)

        files_by_category = summary.get("files_by_category", {})
        documents = files_by_category.get("documents", 0)
        images = files_by_category.get("images", 0)
        other = files_by_category.get("other", 0)

        status_var.set("Status: Preview created successfully")
        summary_var.set(
            f"Scanned: {summary.get('scanned_files', 0)} | "
            f"Documents: {documents} | "
            f"Images: {images} | "
            f"Other: {other} | "
            f"Renames: {summary.get('planned_renames', 0)} | "
            f"Moves: {summary.get('planned_moves', 0)}"
        )

    except subprocess.CalledProcessError:
        status_var.set("Status: Could not create preview")
        summary_var.set("No preview yet")


def open_preview(status_var: tk.StringVar) -> None:
    preview_path = Path(OUTPUT_DIR) / "preview.txt"

    if not preview_path.exists():
        status_var.set("Status: Preview file not found")
        return

    try:
        subprocess.run(["xdg-open", str(preview_path)], check=True)
    except subprocess.CalledProcessError:
        status_var.set("Status: Could not open preview automatically")


def open_preview_folder(status_var: tk.StringVar) -> None:
    output_path = Path(OUTPUT_DIR)

    if not output_path.exists():
        status_var.set("Status: Preview folder not found")
        return

    try:
        subprocess.run(["xdg-open", str(output_path)], check=True)
    except subprocess.CalledProcessError:
        status_var.set("Status: Could not open preview folder")


def main() -> None:
    root = tk.Tk()
    root.title("File Intake Assistant")
    root.geometry("860x560")
    root.configure(padx=20, pady=20)

    folder_var = tk.StringVar(value="")
    status_var = tk.StringVar(value="Status: No folder selected")
    summary_var = tk.StringVar(value="No preview yet")

    title_label = tk.Label(
        root,
        text="File Intake Assistant",
        font=("Arial", 18, "bold"),
    )
    title_label.pack(pady=(0, 10))

    subtitle_label = tk.Label(
        root,
        text="Preview file cleanup before changing anything.",
        font=("Arial", 11),
    )
    subtitle_label.pack(pady=(0, 20))

    warning_label = tk.Label(
        root,
        text="WARNING: MAKE A COPY OF YOUR ORIGINAL FOLDER FIRST",
        font=("Arial", 11, "bold"),
    )
    warning_label.pack(pady=(0, 5))

    preview_only_label = tk.Label(
        root,
        text="This version creates a preview only.",
        font=("Arial", 10),
    )
    preview_only_label.pack(pady=(0, 20))

    selected_folder_title = tk.Label(
        root,
        text="Folder path:",
        font=("Arial", 11),
        anchor="w",
    )
    selected_folder_title.pack(fill="x", pady=(0, 5))

    folder_entry = tk.Entry(
        root,
        textvariable=folder_var,
        font=("Arial", 10),
        width=90,
    )
    folder_entry.pack(fill="x", pady=(0, 15))

    choose_folder_button = tk.Button(
        root,
        text="Choose folder",
        font=("Arial", 11),
        command=lambda: choose_folder(folder_var, status_var, summary_var),
        width=18,
    )
    choose_folder_button.pack(pady=(0, 10))

    preview_button = tk.Button(
        root,
        text="Preview changes",
        font=("Arial", 11),
        command=lambda: run_preview(folder_var, status_var, summary_var),
        width=18,
    )
    preview_button.pack(pady=(0, 10))

    open_preview_button = tk.Button(
        root,
        text="Open preview",
        font=("Arial", 11),
        command=lambda: open_preview(status_var),
        width=18,
    )
    open_preview_button.pack(pady=(0, 10))

    open_preview_folder_button = tk.Button(
        root,
        text="Open preview folder",
        font=("Arial", 11),
        command=lambda: open_preview_folder(status_var),
        width=18,
    )
    open_preview_folder_button.pack(pady=(0, 25))

    status_label = tk.Label(
        root,
        textvariable=status_var,
        font=("Arial", 10),
        anchor="w",
    )
    status_label.pack(fill="x", pady=(10, 5))

    summary_label = tk.Label(
        root,
        textvariable=summary_var,
        font=("Arial", 10),
        anchor="w",
        justify="left",
        wraplength=800,
    )
    summary_label.pack(fill="x")

    root.mainloop()


if __name__ == "__main__":
    main()