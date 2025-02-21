import os
import shutil
import fnmatch
import sys

# Directory to search
TARGET_DIR = "/home/jeff/.local/share/evolution/mail/local"

# Base pattern to match
BASE_PATTERN = ".*"

def delete_matching_items(target_dir, pattern):
    print(f"Starting deletion process in {target_dir} for pattern {pattern}")
    for root, dirs, files in os.walk(target_dir):
        for name in dirs + files:
            if fnmatch.fnmatch(name, pattern):
                item_path = os.path.join(root, name)
                print(f"Found item: {item_path}")
                try:
                    if os.path.isdir(item_path):
                        print(f"Deleting directory {item_path}")
                        shutil.rmtree(item_path)
                    else:
                        print(f"Deleting file {item_path}")
                        os.remove(item_path)
                    print(f"Successfully deleted {item_path}")
                except Exception as e:
                    print(f"Failed to delete {item_path}: {e}")

    print("Deletion process completed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python delete_files_and_folders_spaces_and_wildcards.py <additional_pattern>")
        sys.exit(1)

    additional_pattern = sys.argv[1]
    full_pattern = f"{BASE_PATTERN}{additional_pattern}*"
    delete_matching_items(TARGET_DIR, full_pattern)