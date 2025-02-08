from tkinter import *
from speedtest import Speedtest
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database setup
conn = sqlite3.connect("speedtest_data.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS speed_data (timestamp TEXT, download_speed REAL, upload_speed REAL)")
conn.commit()

def save_data(timestamp, download, upload):
    cursor.execute("INSERT INTO speed_data (timestamp, download_speed, upload_speed) VALUES (?, ?, ?)", (timestamp, download, upload))
    conn.commit()

def fetch_data():
    cursor.execute("SELECT * FROM speed_data")
    return cursor.fetchall()

def speedcheck():
    sp = Speedtest()
    sp.get_servers()
    down = round(sp.download() / (10 ** 6), 2)
    up = round(sp.upload() / (10 ** 6), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update labels
    lab_down.config(text=f"{down} Mbps")
    lab_up.config(text=f"{up} Mbps")
    
    # Save data to database
    save_data(timestamp, down, up)
    
    # Update graph
    update_graph()

def update_graph():
    data = fetch_data()
    timestamps = [row[0] for row in data]
    download_speeds = [row[1] for row in data]
    upload_speeds = [row[2] for row in data]
    
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    ax.plot(timestamps, download_speeds, label="Download Speed (Mbps)", color="#007ACC")
    ax.plot(timestamps, upload_speeds, label="Upload Speed (Mbps)", color="#FF5733")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Speed (Mbps)")
    ax.set_title("Internet Speed Variation Over Time")
    ax.legend(loc="upper left")
    ax.tick_params(axis='x', rotation=45)
    # Embed the graph in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=sp)
    canvas.draw()
    canvas.get_tk_widget().place(x=20, y=540, width=460, height=220)

def on_closing():
    conn.close()
    sp.destroy()

# Tkinter UI
sp = Tk()
sp.title("Internet Speed Test")
sp.geometry("500x800")
sp.config(bg="#1a1a2e")

lab_title = Label(sp, text="Internet Speed Test", font=("Helvetica", 24, "bold"), bg="#1a1a2e", fg="#ffffff")
lab_title.place(x=80, y=40, height=60, width=340)

lab_download = Label(sp, text="Download Speed", font=("Helvetica", 18, "bold"), bg="#1a1a2e", fg="#ffffff")
lab_download.place(x=60, y=150, height=40, width=380)

lab_down = Label(sp, text="0 Mbps", font=("Helvetica", 18, "bold"), bg="#16213e", fg="#ffffff")
lab_down.place(x=60, y=200, height=40, width=380)

lab_upload = Label(sp, text="Upload Speed", font=("Helvetica", 18, "bold"), bg="#1a1a2e", fg="#ffffff")
lab_upload.place(x=60, y=270, height=40, width=380)

lab_up = Label(sp, text="0 Mbps", font=("Helvetica", 18, "bold"), bg="#16213e", fg="#ffffff")
lab_up.place(x=60, y=320, height=40, width=380)

button = Button(sp, text="CHECK SPEED", font=("Helvetica", 18, "bold"), relief=RAISED, bg="#e94560", fg="#ffffff", command=speedcheck)
button.place(x=60, y=420, height=50, width=380)

# Handle closing the app
sp.protocol("WM_DELETE_WINDOW", on_closing)
sp.mainloop()
