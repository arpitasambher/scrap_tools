import subprocess
import json
import time
import os

def run_main_script(user_data: dict):
    """
    Save inputs, run main.py as subprocess, read logs and output JSON.
    """

    # Save user data to input file (if needed by main.py)
    input_path = "/workspace/siriusAI/complete/comp/final/input.json"
    with open(input_path, "w") as f:
        json.dump(user_data, f)

    # Run main.py as subprocess
    process = subprocess.Popen(
        ["python3", "/workspace/siriusAI/complete/comp/final/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    logs = ""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logs += output
            time.sleep(0.1)

    # Read output file
    output_file = "/workspace/siriusAI/complete/comp/final/output/permuted_user_data.json"
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            output_data = json.load(f)
    else:
        output_data = None

    return logs, output_data
