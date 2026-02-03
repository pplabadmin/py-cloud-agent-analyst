"""Script to create a backup of tracked git files."""

import os
import shutil
import subprocess
import sys

MIN_ARGS_COUNT = 2


def copy_tracked_git_files(source_dir: str, dest_dir: str):
    """
    Copies all tracked files from a Git repository to a new directory,
    including the script itself.

    Args:
        source_dir (str): The path to the source Git repository.
        dest_dir (str): The path to the destination folder.
    """
    print(f"Starting copy from '{source_dir}' to '{dest_dir}'...")

    # --- Step 1: Clean the destination directory ---
    # Check if the destination directory exists.
    # Remove it to ensure a clean copy.
    if os.path.exists(dest_dir):
        print("Destination directory exists. Removing old content...")
        try:
            shutil.rmtree(dest_dir)
            print("Old content removed.")
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}")
            return

    # Create the new, clean destination directory.
    os.makedirs(dest_dir)
    print("New destination directory created.")

    # --- Step 2: Get a list of all tracked files from Git ---
    print("Listing tracked files using 'git ls-files'...")
    git_executable = shutil.which("git")
    if not git_executable:
        print(
            "Error: Git command not found. Please ensure Git is "
            "installed and in your PATH."
        )
        return

    # Ensure the executable path is absolute to avoid partial path issues
    git_executable = os.path.abspath(git_executable)

    try:
        # Use subprocess to run the `git ls-files` command.
        # This command lists all files that are tracked by Git, recursively.
        result = subprocess.run(  # nosec  # noqa: S603
            [git_executable, "ls-files"],
            cwd=source_dir,  # Execute the command in the source directory
            check=True,  # Raise an exception if the command fails
            capture_output=True,
            text=True,
            shell=False,
        )
        tracked_files = result.stdout.strip().split("\n")
        print(f"Found {len(tracked_files)} tracked files.")
    except subprocess.CalledProcessError as e:
        print(f"Error running git: {e.stderr.strip()}")
        print("Please ensure you are in a Git repository and have Git installed.")
        return

    # --- Step 3: Copy each tracked file and preserve the folder structure ---
    print("Copying files...")
    for file_path in tracked_files:
        # Construct the full path for both source and destination files.
        source_path = os.path.join(source_dir, file_path)
        dest_path = os.path.join(dest_dir, file_path)

        # Create the subdirectories in the destination if they don't exist.
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Copy the file from source to destination.
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {file_path}")

    # --- Step 4: Copy the script file itself to the destination ---
    script_path = os.path.abspath(__file__)
    script_dest_path = os.path.join(dest_dir, os.path.basename(script_path))
    shutil.copy2(script_path, script_dest_path)
    print(f"Copied script file to: {script_dest_path}")

    print("Copy process completed successfully!")


if __name__ == "__main__":
    script_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(script_dir)

    if len(sys.argv) > MIN_ARGS_COUNT:
        root_source_path = sys.argv[1]
        root_dest_path = sys.argv[2]
    else:
        root_source_path = project_root
        root_dest_path = os.path.join(project_root, "backup")

    copy_tracked_git_files(root_source_path, root_dest_path)
