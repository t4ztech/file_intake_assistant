import sys
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


def choose_folder(
    folder_var: tk.StringVar,
    status_var: tk.StringVar,
    summary_var: tk.StringVar,
    preview_text: tk.Text,
) -> None:
    folder = filedialog.askdirectory(title="Choose folder")
    if not folder:
        return

    folder_var.set(folder)
    status_var.set("Status: Folder selected")
    summary_var.set("No preview yet")

    preview_text.config(state="normal")
    preview_text.delete("1.0", tk.END)
    preview_text.insert(tk.END, "Preview output will appear here after you click 'Preview changes'.")
    preview_text.config(state="disabled")


def run_preview(
    folder_var: tk.StringVar,
    status_var: tk.StringVar,
    summary_var: tk.StringVar,
    preview_text: tk.Text,
) -> None:
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

        preview_text.config(state="normal")
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, "Preview could not be created because the folder path is not valid.")
        preview_text.config(state="disabled")
        return

    try:
        script_path = Path(__file__).with_name("file_intake_assistant_v1.py")

        subprocess.run(
            [
                sys.executable,
                str(script_path),
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
        preview_path = Path(OUTPUT_DIR) / "preview.txt"

        if not summary_path.exists():
            status_var.set("Status: Preview created, but summary not found")
            summary_var.set("No preview yet")

            preview_text.config(state="normal")
            preview_text.delete("1.0", tk.END)
            preview_text.insert(tk.END, "Preview was created, but summary.json was not found.")
            preview_text.config(state="disabled")
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

        preview_content = "Preview file not found."
        if preview_path.exists():
            preview_content = preview_path.read_text(encoding="utf-8")

        preview_text.config(state="normal")
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, preview_content)
        preview_text.config(state="disabled")

    except subprocess.CalledProcessError:
        status_var.set("Status: Could not create preview")
        summary_var.set("No preview yet")

        preview_text.config(state="normal")
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, "Preview could not be created.")
        preview_text.config(state="disabled")


def main() -> None:
    root = tk.Tk()
    root.title("File Intake Assistant")
    root.geometry("980x720")
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

    folder_title_label = tk.Label(
        root,
        text="Folder path:",
        font=("Arial", 11),
        anchor="w",
    )
    folder_title_label.pack(fill="x", pady=(0, 5))

    folder_entry = tk.Entry(
        root,
        textvariable=folder_var,
        font=("Arial", 10),
        width=100,
    )
    folder_entry.pack(fill="x", pady=(0, 15))

    button_frame = tk.Frame(root)
    button_frame.pack(fill="x", pady=(0, 20))

    choose_folder_button = tk.Button(
        button_frame,
        text="Choose folder",
        font=("Arial", 11),
        width=18,
    )
    choose_folder_button.pack(side="left", padx=(0, 10))

    preview_button = tk.Button(
        button_frame,
        text="Preview changes",
        font=("Arial", 11),
        width=18,
    )
    preview_button.pack(side="left")

    status_label = tk.Label(
        root,
        textvariable=status_var,
        font=("Arial", 10),
        anchor="w",
    )
    status_label.pack(fill="x", pady=(0, 5))

    summary_label = tk.Label(
        root,
        textvariable=summary_var,
        font=("Arial", 10),
        anchor="w",
        justify="left",
        wraplength=920,
    )
    summary_label.pack(fill="x", pady=(0, 22))

    preview_title_label = tk.Label(
        root,
        text="Preview details:",
        font=("Arial", 11),
        anchor="w",
    )
    preview_title_label.pack(fill="x", pady=(0, 8))

    preview_frame = tk.Frame(root)
    preview_frame.pack(fill="both", expand=True)

    preview_scrollbar = tk.Scrollbar(preview_frame)
    preview_scrollbar.pack(side="right", fill="y")

    preview_text = tk.Text(
        preview_frame,
        wrap="word",
        font=("Courier New", 12),
        yscrollcommand=preview_scrollbar.set,
    )
    preview_text.pack(side="left", fill="both", expand=True)
    preview_scrollbar.config(command=preview_text.yview)

    preview_text.insert("1.0", "Preview output will appear here after you click 'Preview changes'.")
    preview_text.config(state="disabled")

    choose_folder_button.config(
        command=lambda: choose_folder(folder_var, status_var, summary_var, preview_text)
    )
    preview_button.config(
        command=lambda: run_preview(folder_var, status_var, summary_var, preview_text)
    )

    root.mainloop()


if __name__ == "__main__":
    main()