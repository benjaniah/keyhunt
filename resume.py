#!/usr/bin/env python3
import subprocess
import signal
import sys
import os

RUN_FILE = "run.sh"
LOG_FILE = "run.log"

# Track interrupted state
interrupted = False
def handle_interrupt(sig, frame):
    global interrupted
    print("\n[Interrupted]")
    interrupted = True

signal.signal(signal.SIGINT, handle_interrupt)
signal.signal(signal.SIGTERM, handle_interrupt)

# Read completed lines
completed = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        completed = set(line.rstrip("\n") for line in f)

# Read all lines
with open(RUN_FILE, "r") as f:
    lines = [line.rstrip("\n") for line in f if line.strip()]

for lineno, line in enumerate(lines, start=1):
    if interrupted:
        print(f"Stopping at line {lineno} due to interrupt.")
        break

    if line in completed:
        print(f"Skipping line {lineno}: {line}")
        continue

    print(f"Running line {lineno}: {line}")
    try:
        # Run the command and stream stdout/stderr
        process = subprocess.Popen(line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for output_line in process.stdout:
            print(output_line, end="")  # print output as it comes
        process.wait()
        if process.returncode != 0:
            print(f"Command failed at line {lineno}: {line}")
            sys.exit(1)
    except Exception as e:
        print(f"Error running line {lineno}: {e}")
        sys.exit(1)

    # Log successful line
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(f"Completed line {lineno}")

print("All done (or interrupted).")
