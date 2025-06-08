import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# File paths
csv_path = '/home/blane/website/outputs.csv'
output_dir = '/home/blane/website/'

# Load the CSV data
df = pd.read_csv(csv_path)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

### ----- Uptime Graph -----
uptime_df = df[df['Command'] == 'uptime'].copy()
uptime_df['Load1'] = uptime_df['Output'].str.extract(r'load average: ([0-9.]+)')[0].astype(float)
uptime_df['Load5'] = uptime_df['Output'].str.extract(r'load average: [0-9.]+, ([0-9.]+)')[0].astype(float)
uptime_df['Load15'] = uptime_df['Output'].str.extract(r'load average: [0-9.]+, [0-9.]+, ([0-9.]+)')[0].astype(float)

plt.figure(figsize=(10, 5))
plt.plot(uptime_df['Timestamp'], uptime_df['Load1'], label='1 min')
plt.plot(uptime_df['Timestamp'], uptime_df['Load5'], label='5 min')
plt.plot(uptime_df['Timestamp'], uptime_df['Load15'], label='15 min')
plt.title('Uptime Load Averages')
plt.xlabel('Time')
plt.ylabel('Load')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'uptime_load_graph.png'))
plt.close()

### ----- Disk Usage Graph (/ /var /home) -----
df_df = df[df['Command'] == 'df -h'].copy()
df_df = df_df.dropna()

mount_points = ['/', '/var', '/home']
disk_data = {mp: [] for mp in mount_points}

for ts in df_df['Timestamp'].unique():
    ts_df = df_df[df_df['Timestamp'] == ts]
    for mp in mount_points:
        match = ts_df['Output'].str.extract(rf'{mp}\s+\S+\s+\S+\s+\S+\s+(\d+)%')
        usage = match.dropna().squeeze()
        if not usage.empty:
            disk_data[mp].append((ts, int(usage)))
        else:
            disk_data[mp].append((ts, None))  # In case mount not found

plt.figure(figsize=(10, 5))
for mp, color in zip(mount_points, ['blue', 'green', 'purple']):
    timestamps, usages = zip(*disk_data[mp])
    alert_color = ['red' if (u is not None and u > 90) else color for u in usages]
    for i in range(1, len(timestamps)):
        if usages[i - 1] is not None and usages[i] is not None:
            plt.plot(timestamps[i-1:i+1], usages[i-1:i+1],
                     color=alert_color[i], label=mp if i == 1 else "", linewidth=2)

plt.title('Disk Usage: /, /var, /home')
plt.xlabel('Time')
plt.ylabel('% Used')
plt.ylim(0, 100)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'disk_usage_combined.png'))
plt.close()

### ----- NTP Offset Graph w/ PPS Sync Check -----
ntpq_df = df[df['Command'].str.contains("ntpq")].copy()
ntpq_df = ntpq_df.dropna(subset=['Output'])

ntpq_df['Offset'] = ntpq_df['Output'].str.extract(r'\*\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+([-0-9.]+)')[0]
ntpq_df['Offset'] = pd.to_numeric(ntpq_df['Offset'], errors='coerce')

plt.figure(figsize=(10, 5))
color = 'blue' if any(ntpq_df['Output'].str.contains('PPS')) else 'red'
plt.plot(ntpq_df['Timestamp'], ntpq_df['Offset'], label='NTP Offset', color=color)
plt.title(f'NTP Offset {"(PPS Synced)" if color == "blue" else "(Not Synced)"}')
plt.xlabel('Time')
plt.ylabel('Offset (ms)')
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'ntp_offset.png'))
plt.close()

### ----- HTML Dashboard -----
html_path = os.path.join(output_dir, 'index.html')
with open(html_path, 'w') as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
  <title>Server Monitoring Dashboard</title>
  <style>
    body {{ font-family: Arial; background: #111; color: #ddd; text-align: center; }}
    img {{ width: 90%; max-width: 800px; margin: 20px auto; display: block; border: 1px solid #333; }}
    h2 {{ margin-top: 40px; }}
  </style>
</head>
<body>
  <h1>Server Monitoring Dashboard</h1>
  <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  <h2>Uptime Load Averages</h2>
  <img src="uptime_load_graph.png" alt="Uptime Load Averages">
  <h2>Disk Usage</h2>
  <img src="disk_usage_combined.png" alt="Disk Usage Combined">
  <h2>NTP Offset</h2>
  <img src="ntp_offset.png" alt="NTP Offset">
</body>
</html>
""")

