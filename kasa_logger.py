import asyncio
import csv
import os
from datetime import datetime
from kasa import Discover, Module

# --- CONFIGURATION ---
PLUG_IP = "192.168.1.237" # Replace with your plug's IP
CSV_FILE = "server_power_usage.csv"

async def main():
    try:
        # Connect using the new discover_single method (fixes the SmartPlug warning)
        plug = await Discover.discover_single(PLUG_IP)
        await plug.update()

        # Check if the plug supports the new Energy module
        if Module.Energy not in plug.modules:
            print("Error: This Kasa plug model does not support energy monitoring.")
            return

        # Pull the data using the updated syntax (fixes the emeter_this_month warning)
        plug_name = plug.alias
        monthly_kwh = plug.modules[Module.Energy].consumption_this_month
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Check if the CSV file already exists so we know whether to write headers
        file_exists = os.path.isfile(CSV_FILE)

        # Open the CSV file and append the new data
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write column headers if it's a brand new file
            if not file_exists:
                writer.writerow(["Date", "Plug Name", "Month-to-Date Usage (kWh)"])

            # Write the data row
            writer.writerow([today_date, plug_name, monthly_kwh])

        print(f"Success! Logged {monthly_kwh} kWh for '{plug_name}' on {today_date}.")

    except Exception as e:
        print(f"Failed to connect or log data: {e}")

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
