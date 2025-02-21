#!/bin/bash

# Directory where the mbox files are located
MBOX_DIR="/home/jeff/Documents/mbox/Offline"

# Evolution mail directory
EVOLUTION_MAIL_DIR="$HOME/.local/share/evolution/mail/local"

# Temporary directory for conversion
TMP_DIR="$HOME/tmp"

# Log file for import process
LOG_FILE="$HOME/Documents/mbox/import_log.txt"
echo "Import log file: $LOG_FILE"

# Ensure the temporary directory exists
mkdir -p "$TMP_DIR"

# Function to convert mbox files to Maildir format and move them to Evolution
convert_and_move() {
    local mbox_file="$1"
    echo "Processing $mbox_file..." | tee -a "$LOG_FILE"
    local relative_path="${mbox_file#$MBOX_DIR/}"
    echo "Relative path: $relative_path" | tee -a "$LOG_FILE"
    local folder_name="${relative_path//\//.}"
    folder_name="${folder_name%.mbox}"
    echo "Folder name: $folder_name" | tee -a "$LOG_FILE"
    local maildir_path="$EVOLUTION_MAIL_DIR/.jeff-22ndtech-offline.${folder_name}"
    echo "Maildir path: $maildir_path" | tee -a "$LOG_FILE"

    # Check if the maildir_path already exists
    if [ -d "$maildir_path" ]; then
        echo "Maildir path $maildir_path already exists. Skipping..." | tee -a "$LOG_FILE"
        return 0
    fi

    echo "Converting $mbox_file to Maildir format..." | tee -a "$LOG_FILE"
    mb2md -s "$mbox_file" -d "$TMP_DIR/maildir" 2>>"$LOG_FILE"
    if [ $? -ne 0 ]; then
        echo "Failed to convert $mbox_file" | tee -a "$LOG_FILE"
        return 1
    fi

    # Create the Maildir structure
    echo "CREATING Maildir structure at $maildir_path..." | tee -a "$LOG_FILE"
    mkdir -p "$maildir_path/cur" "$maildir_path/new" "$maildir_path/tmp"
    if [ $? -ne 0 ]; then
        echo "Failed to create Maildir structure at $maildir_path" | tee -a "$LOG_FILE"
        return 1
    fi

    echo "Moving converted Maildir to $maildir_path..." | tee -a "$LOG_FILE"
    if [ -d "$TMP_DIR/maildir/cur" ]; then
        mv "$TMP_DIR/maildir/cur/"* "$maildir_path/cur/" 2>>"$LOG_FILE"
    fi
    if [ -d "$TMP_DIR/maildir/new" ]; then
        mv "$TMP_DIR/maildir/new/"* "$maildir_path/new/" 2>>"$LOG_FILE"
    fi
    if [ -d "$TMP_DIR/maildir/tmp" ]; then
        mv "$TMP_DIR/maildir/tmp/"* "$maildir_path/tmp/" 2>>"$LOG_FILE"
    fi

    if [ $? -ne 0 ]; then
        echo "Failed to move Maildir to $maildir_path" | tee -a "$LOG_FILE"
        return 1
    fi

    echo "Creating metadata files at $maildir_path..." | tee -a "$LOG_FILE"
    touch "$maildir_path/.cmeta"
    touch "$maildir_path/.ibex.index"
    touch "$maildir_path/.ibex.index.data"
    if [ $? -ne 0 ]; then
        echo "Failed to create metadata files at $maildir_path" | tee -a "$LOG_FILE"
        return 1
    fi
}

# Function to process mbox files recursively
process_mbox_files() {
    local dir="$1"
    for file in "$dir"/*; do
        echo "Processing $file" | tee -a "$LOG_FILE"
        if [ -d "$file" ]; then
            echo "$file is a directory" | tee -a "$LOG_FILE"
            process_mbox_files "$file"
        elif [[ "$(basename "$file")" == "mbox" ]]; then
            echo "$file is an mbox file" | tee -a "$LOG_FILE"
            convert_and_move "$file"
        else
            echo "$file is not an mbox file" | tee -a "$LOG_FILE"
        fi
    done
}

# Start the conversion and import process
echo "Starting import process..." | tee "$LOG_FILE"
process_mbox_files "$MBOX_DIR"

# Notify the user
echo "Import process completed. You can now open Evolution." | tee -a "$LOG_FILE"