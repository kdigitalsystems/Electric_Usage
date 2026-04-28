import asyncio
import csv
import os
from datetime import datetime
import pytz
from kasa import SmartPlug

# --- CONFIGURATION ---
DEVICE_IP = "192.168.1.237"
TIMEZONE = "America/Chicago"  # Fulshear, Texas
LOG_FILE = "server_power_usage_plug1.csv"

async def record_usage():
    try:
        # 1. Setup Timezone and Plug
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        
        plug = SmartPlug(DEVICE_IP)
        await plug.update()

        # 2. Gather Data
        # Timestamp with TZ abbreviation (e.g., 2026-04-21 23:19:00 CDT)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        # Real-time Watts (Hourly snapshot)
        current_watts = plug.emeter_realtime.power 
        
        # Daily Total (Total kWh used since midnight)
        daily_kwh = plug.emeter_today
        
        # Monthly Total (Total kWh used since the 1st)
        monthly_kwh = plug.emeter_this_month

        # 3. Prepare CSV
        headers = ["Timestamp", "Watts_Realtime", "Daily_Total_kWh", "Monthly_Total_kWh"]
        row = [timestamp, current_watts, daily_kwh, monthly_kwh]

        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(row)

        print(f"[{timestamp}] Saved to {LOG_FILE}: {current_watts}W | {daily_kwh}kWh Day | {monthly_kwh}kWh Month")

    except Exception as e:
        print(f"Error connecting to Kasa plug: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(record_usage())
