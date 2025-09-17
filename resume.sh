#!/bin/bash

LOGFILE="run.log"

while IFS= read -r line; do
    # Skip empty lines
    [[ -z "$line" ]] && continue
    
    # Skip if line already completed
    if grep -Fxq "$line" "$LOGFILE" 2>/dev/null; then
        echo "Skipping already done: $line"
        continue
    fi
    
    echo "Running: $line"
    if eval "$line"; then
        echo "$line" >> "$LOGFILE"
    else
        echo "Command failed: $line"
        exit 1
    fi
done < run.sh
