from pynput.keyboard import Key, Listener
import json
import threading
import time
import os
import subprocess

# Loads DB
db_path = "../db/counter.json"
config_path = "../db/settings.json"
click_path = "../resources/click.mp3"
ding_path = "../resources/ding2.mp3"

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
def on_press(key):
    
    print(key)
    total = update_counter(key)
    if config_parsed["sfx"]:
        if str(key) == "Key.enter":
            subprocess.Popen(["afplay", ding_path])
        else:
            subprocess.Popen(["afplay", click_path])
    

# Collect events until released
def init():
    threading.Thread(target=saveDB, daemon=True).start()
    listener = Listener(on_press=on_press)
    listener.start()
    return listener


# init()