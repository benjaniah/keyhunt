#!/bin/bash

LOGFILE="run.log"

lineno=0
while IFS= read -r line; do
    ((lineno++))  # keep track of line number
    
    # Skip empty lines
    [[ -z "$line" ]] && continue
    
    # Skip if line already completed
    if grep -Fxq "$line" "$LOGFILE" 2>/dev/null; then
        echo "Skipping line $lineno: $line"
        continue
    fi
    
    echo "Running line $lineno: $line"
    if eval "$line"; then
        echo "$line" >> "$LOGFILE"
    else
        echo "Command failed at line $lineno: $line"
        exit 1
    fi
done < run.sh
