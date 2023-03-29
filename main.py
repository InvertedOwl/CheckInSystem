import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter import simpledialog
import json
import os.path
import schedule
import random


# Acquire data
if os.path.isfile("hours.json"):
    f = open("hours.json", "r")
    h = open("namesRe.json", "r")
    hours = json.loads(f.read())
    namesRe = json.loads(h.read())
else:
    namesRe = {}
    hours = {}

ids = {}

# Create some random data to plot
name = namesRe.values()
y_data = hours.values()

# Sort the data in descending order
data = sorted(zip(name, y_data), key=lambda pair: pair[1], reverse=False)
names, y_data = zip(*data)
print(names)
print(y_data)

# Create a tkinter window and set it to fullscreen
root = tk.Tk()
root.attributes('-fullscreen', True)

def generate_random_colors(num):
    colors = ["#D0C9C0", "#EFEAD8", "#6D8B74", "#5F7161"]
    # Shuffle the list of colors
    random.shuffle(colors)
    # Repeat the list if num is greater than the length of the list
    if num > len(colors):
        colors = colors * (num // len(colors) + 1)
    # Slice the list
    result = colors[:num]
    return result

# Create a matplotlib figure and plot the data as a horizontal bar graph
fig = plt.Figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
ax.barh(names, y_data, color=generate_random_colors(len(y_data)))

# Set the x-axis and y-axis labels
ax.set_xlabel("Hours")
ax.set_ylabel("")
ax.set_title("Check In/Out", fontsize=60)
print((5 * int(y_data[len(y_data) - 1]) / 100))
if (5 * int(y_data[len(y_data) - 1]) / 100) <= 0.5:
    ax.set_xticks(range(0, int(y_data[len(y_data) - 1]) + 1, 1))
else:
    ax.set_xticks(range(0, int(y_data[len(y_data) - 1]) + int(round(5 * int(y_data[len(y_data) - 1]) / 100)), int(round(5 * int(y_data[len(y_data) - 1]) / 100))))

# Create a tkinter canvas and add the matplotlib figure to it
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a button to exit the program
button = tk.Button(root, text="Exit", command=root.destroy)
button.pack(side=tk.BOTTOM)

# Create a label to display the typed numbers
label = tk.Label(root, text="")
label.pack(side=tk.BOTTOM)


# Function to handle key press events
def onKey(event):
    if event.char.isdigit():
        label.config(text=label.cget("text") + event.char)


# Function to handle "Enter" key press events
def onEnter(event):
    number = label.cget("text")
    if number:

        # If they are not logged in
        if number not in ids or ids[number] is None:
            ids[number] = datetime.now().timestamp()

            # If they do not have a name
            if number not in namesRe:
                name = simpledialog.askstring("Input", "What is your name",
                                              parent=root)
                namesRe[number] = name
                namesReFile = open("namesRe.json", 'w')
                namesReFile.write(json.dumps(namesRe))
                namesReFile.close()

        # If they are logged in
        else:
            tempHours = (datetime.now().timestamp() - ids[number]) / 3600
            if number in hours:
                hours[number] = float(hours[number]) + tempHours
            else:
                hours[number] = tempHours

            # Set data
            namesReFile2 = open("hours.json", 'w')
            namesReFile2.write(json.dumps(hours))
            namesReFile2.close()
            ids[number] = None
            name2 = namesRe.values()
            y_data2 = hours.values()
            data2 = sorted(zip(name2, y_data2), key=lambda pair: pair[1], reverse=False)
            names2, y_data2 = zip(*data2)
            print(names2)
            print(y_data2)

            # Reset bar graphs
            ax.clear()
            ax.barh(names2, y_data2, color=generate_random_colors(len(y_data)))
            ax.set_xlabel("Hours")
            ax.set_ylabel("")
            ax.set_title("Check In/Out", fontsize=60)
            canvas.draw()

        label.config(text="")


# Bind key press events to functions
root.bind('<KeyPress>', onKey)
root.bind('<Return>', onEnter)

# Checks time
def loop():
    schedule.run_pending()
    root.after(33, loop)

# Log everyone out at certain times
def clearAll():
    print("AUTO SIGN OUT")
    for number in ids:
        if not ids[number] is None:
            print(number)
            tempHours = (datetime.now().timestamp() - ids[number]) / 3600
            if number in hours:
                hours[number] = float(hours[number]) + tempHours
            else:
                hours[number] = tempHours
            namesReFile2 = open("hours.json", 'w')
            namesReFile2.write(json.dumps(hours))
            namesReFile2.close()
            ids[number] = None
            name2 = namesRe.values()
            y_data2 = hours.values()
            data2 = sorted(zip(name2, y_data2), key=lambda pair: pair[1], reverse=False)
            names2, y_data2 = zip(*data2)
            print(names2)
            print(y_data2)

            ax.clear()
            ax.barh(names2, y_data2, color=generate_random_colors(len(y_data)))
            ax.set_xlabel("Hours")
            ax.set_ylabel("")
            ax.set_title("Check In/Out", fontsize=60)
            canvas.draw()


schedule.every().day.at("17:00").do(clearAll)
schedule.every().day.at("19:00").do(clearAll)
schedule.every().day.at("12:30").do(clearAll)

root.after(33, loop)
# Start the tkinter mainloop
root.mainloop()
