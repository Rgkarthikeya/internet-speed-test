import sqlite3
import matplotlib.pyplot as plt
from tabulate import tabulate

# Connect to the database
conn = sqlite3.connect("speedtest_data.db")
cursor = conn.cursor()

# Fetch all data
cursor.execute("SELECT * FROM speed_data")
rows = cursor.fetchall()

# Display the data in a formatted table
headers = ["Timestamp", "Download Speed (Mbps)", "Upload Speed (Mbps)"]
print(tabulate(rows, headers=headers, tablefmt="pretty"))

# Extract data for plotting
timestamps = [row[0] for row in rows]
download_speeds = [row[1] for row in rows]
upload_speeds = [row[2] for row in rows]

# Find the highest download and upload speeds
max_download = max(download_speeds)
max_upload = max(upload_speeds)
max_download_time = timestamps[download_speeds.index(max_download)]
max_upload_time = timestamps[upload_speeds.index(max_upload)]

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, download_speeds, label="Download Speed (Mbps)", color="blue", marker="o")
plt.plot(timestamps, upload_speeds, label="Upload Speed (Mbps)", color="green", marker="o")

# Highlight the highest points
plt.annotate(f"Max Download: {max_download} Mbps", 
             xy=(max_download_time, max_download), 
             xytext=(max_download_time, max_download + 5), 
             arrowprops=dict(facecolor='blue', shrink=0.05))

plt.annotate(f"Max Upload: {max_upload} Mbps", 
             xy=(max_upload_time, max_upload), 
             xytext=(max_upload_time, max_upload + 5), 
             arrowprops=dict(facecolor='green', shrink=0.05))

# Labels and title
plt.xlabel("Timestamp")
plt.ylabel("Speed (Mbps)")
plt.title("Internet Speed Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()

# Close the database connection
conn.close()
'''
import sqlite3
from tabulate import tabulate

# Connect to the database
conn = sqlite3.connect("speedtest_data.db")
cursor = conn.cursor()

# Fetch all data
cursor.execute("SELECT * FROM speed_data")
rows = cursor.fetchall()

# Display the data in a formatted table
headers = ["Timestamp", "Download Speed (Mbps)", "Upload Speed (Mbps)"]
print(tabulate(rows, headers=headers, tablefmt="pretty"))

# Close the database connection
conn.close()


'''
