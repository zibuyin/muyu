from pynput.keyboard import Key, Listener
import json
import threading
import time
import os
import subprocess
import random
import shutil
import sys

# Paths for local development vs bundled app.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    bundle_root = getattr(sys, "_MEIPASS")
else:
    bundle_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app_data_dir = os.path.expanduser("~/Library/Application Support/muyu")
os.makedirs(app_data_dir, exist_ok=True)

default_db_path = os.path.join(bundle_root, "db", "counter.json")
default_config_path = os.path.join(bundle_root, "db", "settings.json")

db_path = os.path.join(app_data_dir, "counter.json")
config_path = os.path.join(app_data_dir, "settings.json")
click_path = os.path.join(bundle_root, "resources", "click2.mp3")
ding_path = os.path.join(bundle_root, "resources", "ding2.mp3")


def ensure_json_file(target_path, source_path, default_payload):
    if os.path.exists(target_path):
        return

    if os.path.exists(source_path):
        shutil.copyfile(source_path, target_path)
        return

    with open(target_path, 'w') as file:
        json.dump(default_payload, file)


ensure_json_file(db_path, default_db_path, {"total": 0})
ensure_json_file(config_path, default_config_path, {"sfx": True})

with open(db_path, 'r') as db:
    db_parsed = json.load(db)
print(db_parsed)
with open(config_path, 'r') as config:
    config_parsed = json.load(config)
print(config_parsed)

lock = threading.Lock()
# Update counter
def update_counter(key):
    global db_parsed
    with lock:
        # Increase total key presses
        db_parsed["total"] += 1

        # Clean 'a' => a
        parsed_key =  str(key).replace("'","")
        try:
            db_parsed[parsed_key] += 1
        except KeyError:
            print("Unknown key")

        print(db_parsed["total"])
        pass
        
        
        return db_parsed["total"]


def saveDB():
    print("DEBUG")
    while True:
        time.sleep(10)
        with lock:
            with open(db_path, 'w') as db:
                    # db_parsed is the Python dict of the keypresses data
                    json.dump(db_parsed, db)
        print("Saved!")


def clearDB():
    with lock:
        print("CLEARING DB")
        for _, key in enumerate(db_parsed):
            db_parsed[key] = 0
        with open(db_path, 'w') as db:
            json.dump(db_parsed, db)




def getDB():
    with lock:
        return db_parsed


def play_keypress_sfx(path, *, pitch_jitter=0.07, volume_jitter=0.08):
    # Add slight randomization so repeated presses sound less robotic.
    rate = 1.0 + random.uniform(-pitch_jitter, pitch_jitter)
    volume = 1.0 - random.uniform(0, volume_jitter)
    subprocess.Popen([
        "afplay",
        "-r",
        f"{rate:.3f}",
        "-v",
        f"{volume:.2f}",
        path,
    ])


def on_press(key):
    
    print(key)
    total = update_counter(key)
    if config_parsed["sfx"]:
        if str(key) == "Key.enter":
            play_keypress_sfx(ding_path, pitch_jitter=0.02, volume_jitter=0.06)
        else:
            play_keypress_sfx(click_path)
    

# Collect events until released
def init():
    threading.Thread(target=saveDB, daemon=True).start()
    listener = Listener(on_press=on_press)
    listener.start()
    return listener


# init()