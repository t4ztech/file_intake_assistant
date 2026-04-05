import json
import re
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


OUTPUT_DIR = "gui_preview_output"


def normalize_folder_path(raw_path: str) -> str:
    path = raw_path.strip()

    windows_match = re.match(r"^([A-Za-z]):\\", path)
    if windows_match:
        drive_letter = windows_match.group(1).lower()
        rest = path[2:].replace("\\", "/")
        return f"/mnt/{drive_letter}{rest}"

    return path


def reset_preview_box(preview_text: tk.Text, text: str) -> None:
    preview_text.config(state="normal")
    preview_text.delete("1.0", tk.END)
    preview_text.insert(tk.END, text)
    preview_text.config(state="disabled")


def choose_folder(
    folder_var: tk.StringVar,
    status_var: tk.StringVar,
    summary_var: tk.StringVar,
    preview_text: tk.Text,
    preview_ready_var: tk.BooleanVar,
) -> None:
    folder = filedialog.askdirectory(title="Choose folder")
    if not folder:
        return

    folder_var.set(folder)
    status_var.set("Status: Folder selected")
    summary_var.set("No preview yet")
    preview_ready_var.set(False)

    reset_preview_box(
        preview_text,
        "Preview output will appear here after you click 'Preview changes'.",
    )


def run_tool(
    folder: str,
    apply_changes: bool,
) -> tuple[bool, str]:
    script_path = Path(__file__).with_name("file_intake_assistant_v1.py")

    cmd = [
        sys.executable,
        str(script_path),
        "--root",
        folder,
        "--output-dir",
        OUTPUT_DIR,
    ]

    if apply_changes:
        cmd.append("--apply")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip() or e.stdout.strip() or "Unknown error."
        return False, error_output


def update_summary_and_preview(
    status_var: tk.StringVar,
    summary_var: tk.StringVar,
    preview_text: tk.Text,
    status_message: str,
    fallback_preview_text: str,
) -> None:
    summary_path = Path(OUTPUT_DIR) / "summary.json"
    preview_path = Path(OUTPUT_DIR) / "preview.txt"

    if summary_path.exists():
        with summary_path.open("r", encoding="utf-8") as f:
            summary = json.load(f)

        files_by_category = summary.get("files_by_category", {})
        documents = files_by_category.get("documents", 0)
        images = files_by_category.get("images", 0)
        other = files_by_category.get("other", 0)

        summary_var.set(
            f"Scanned: {summary.get('scanned_files', 0)} | "
            f"Documents: {documents} | "
            f"Images: {images} | "
            f"Other: {other} | "
            f"Renames: {summary.get('planned_renames', 0)} | "
            f"Moves: {summary.get('planned_moves', 0)}"
        )
    else:
        summary_var.set("No preview yet")

    preview_content = fallback_preview_text
    if preview_path.exists():
        preview_content = preview_path.read_text(encoding="utf-8")

    status_var.set(status_message)
    reset_preview_box(preview_text, preview_content)


def run_preview(
    folder_var: tk.StringVar,
    status_var: tk.StringVar,
    summary_var: tk.StringVar,
    preview_text: tk.Text,
    preview_ready_var: tk.BooleanVar,
) -> None:
    raw_folder = folder_var.get().strip()

    if not raw_folder:
        status_var.set("Status: No folder selected")
        summary_var.set("No preview yet")
        preview_ready_var.set(False)
        reset_preview_box(
            preview_text,
            "Preview output will appear here after you click 'Preview changes'.",
        )
        return

    folder = normalize_folder_path(raw_folder)
    folder_var.set(folder)

    folder_path = Path(folder)
    if not folder_path.exists() or not folder_path.is_dir():
        status_var.set("Status: Folder path is not valid")
        summary_var.set("No preview yet")
        preview_ready_var.set(False)

        reset_preview_box(
            preview_text,
            "Preview could not be created because the folder path is not valid.",
        )
        return

    ok, output = run_tool(folder, apply_changes=False)

    if not ok:
        status_var.set("Status: Could not create preview")
        summary_var.set("No preview yet")
        preview_ready_var.set(False)
        reset_preview_box(preview_text, output)
        return

    preview_ready_var.set(True)
    update_summary_and_preview(
        status_var,
        summary_var,
        preview_text,
        "Status: Preview created successfully",
        output or "Preview created successfully.",
    )


def apply_changes(
    folder_var: tk.StringVar,
    status_var: tk.StringVar,
    summary_var: tk.StringVar,
    preview_text: tk.Text,
    preview_ready_var: tk.BooleanVar,
) -> None:
    raw_folder = folder_var.get().strip()

    if not raw_folder:
        status_var.set("Status: No folder selected")
        return

    if not preview_ready_var.get():
        status_var.set("Status: Create a preview first")
        return

    folder = normalize_folder_path(raw_folder)
    folder_var.set(folder)

    folder_path = Path(folder)
    if not folder_path.exists() or not folder_path.is_dir():
        status_var.set("Status: Folder path is not valid")
        return

    confirmed = messagebox.askokcancel(
        title="Apply changes",
        message=(
            "This will rename and move files in the selected folder.\n\n"
            "Use this only on a copied test folder.\n\n"
            "Do you want to continue?"
        ),
    )

    if not confirmed:
        status_var.set("Status: Apply cancelled")
        return

    ok, output = run_tool(folder, apply_changes=True)

    if not ok:
        status_var.set("Status: Apply could not be completed")
        reset_preview_box(preview_text, output)
        return

    preview_ready_var.set(False)
    update_summary_and_preview(
        status_var,
        summary_var,
        preview_text,
        "Status: Apply completed successfully",
        output or "Apply completed successfully.",
    )


def main() -> None:
    root = tk.Tk()
    root.title("File Intake Assistant")
    root.geometry("980x720")
    root.configure(padx=20, pady=20)

    folder_var = tk.StringVar(value="")
    status_var = tk.StringVar(value="Status: No folder selected")
    summary_var = tk.StringVar(value="No preview yet")
    preview_ready_var = tk.BooleanVar(value=False)

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
        text="This version lets you preview and apply changes.",
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
    preview_button.pack(side="left", padx=(0, 10))

    apply_button = tk.Button(
        button_frame,
        text="Apply changes",
        font=("Arial", 11),
        width=18,
    )
    apply_button.pack(side="left")

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
        command=lambda: choose_folder(
            folder_var, status_var, summary_var, preview_text, preview_ready_var
        )
    )
    preview_button.config(
        command=lambda: run_preview(
            folder_var, status_var, summary_var, preview_text, preview_ready_var
        )
    )
    apply_button.config(
        command=lambda: apply_changes(
            folder_var, status_var, summary_var, preview_text, preview_ready_var
        )
    )

    root.mainloop()


if __name__ == "__main__":
    main()