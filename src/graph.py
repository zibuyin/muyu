import matplotlib.pyplot as plt
import numpy as np
import string

letters = list(string.ascii_lowercase)


def plotKeyboard(db):
    x_axis = []
    y_axis = []
    
    for _, key in enumerate(db):
        # Ignore "total" and special keys
        if key == "total":
            pass
        
        elif "Key" in key:
            pass
        elif key in letters:
            x_axis.append(key)
            y_axis.append(db[key])
        

    # Define the graph
    plt.bar(x_axis, y_axis)
    plt.title("Key Presses Distribution")
    plt.xlabel("Keys")
    plt.ylabel("Count")
    plt.show()