#!/usr/bin/python3
#
# This script
# - checks the status in the network of the switch
# - changes the values
# - uploads the current status
#
import json
import os
import subprocess

HERE = os.path.dirname(__file__) or "."
DATA = os.path.join(HERE, "api.json")
STATUS = os.path.join(HERE, "status.sh")

subprocess.call(["git", "pull"], cwd=HERE)

with open(DATA) as f:
    data = json.load(f)

is_open = subprocess.call([STATUS]) == 0

has_changed = data["state"]["open"] != is_open
data["state"]["open"] = is_open

print("Status " + ("changed to " if has_changed else "remains ") + ("open" if is_open else "closed") + ".")

if has_changed:
    with open(DATA, "w") as f:
        json.dump(data, f, indent=4)
    subprocess.check_call(["git", "add", "api.json"], cwd=HERE)
    subprocess.check_call(["git", "commit", "-m", "automatic status update"], cwd=HERE)
    subprocess.call(["git", "push"], cwd=HERE)
