import multiprocessing as mp
import string

letters = list(string.ascii_lowercase)


def _render_graph_window(x_axis, y_axis):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.bar(x_axis, y_axis)
    ax.set_title("Key Presses Distribution")
    ax.set_xlabel("Keys")
    ax.set_ylabel("Count")
    plt.show()


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
        

    # Use a child process so closing the plot window does not affect the menubar app.
    process = mp.Process(target=_render_graph_window, args=(x_axis, y_axis), daemon=True)
    process.start()