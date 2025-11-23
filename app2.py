import time
from datetime import datetime as dt
import os

# --- Configuration ---
# Enter the sites you want to block
sites_to_block = [
    "www.facebook.com",
    "facebook.com",
    "www.youtube.com",
    "youtube.com",
    "www.gmail.com",
    "gmail.com",
]

# Define the redirect IP (Localhost)
redirect_ip = "127.0.0.1"

# Define the working hours (24-hour format)
START_HOUR = 9
END_HOUR = 21

# --- OS Host File Path Logic ---
LINUX_HOST = "/etc/hosts"
WINDOWS_HOST = r"C:\Windows\System32\drivers\etc\hosts"

if os.name == 'posix':
    DEFAULT_HOSTER = LINUX_HOST
elif os.name == 'nt':
    DEFAULT_HOSTER = WINDOWS_HOST
else:
    print("OS Unknown. Exiting.")
    exit()

def block_websites(start_hour, end_hour):
    """
    Manages the blocking and unblocking of websites based on the specified hours.
    """
    while True:
        current_time = dt.now()
        
        # Define the work day start and end datetimes for today
        start_of_work = dt(current_time.year, current_time.month, current_time.day, start_hour)
        end_of_work = dt(current_time.year, current_time.month, current_time.day, end_hour)

        try:
            # --- Blocking Logic: Within Working Hours ---
            if start_of_work < current_time < end_of_work:
                print(f"[{current_time.strftime('%H:%M:%S')}] 🔴 WORKING TIME: Websites blocked.")
                
                with open(DEFAULT_HOSTER, "r+") as hostfile:
                    content = hostfile.read()
                    
                    # Check and add sites if they are not already present
                    for site in sites_to_block:
                        # Ensures that we don't duplicate the block entry
                        if site not in content:
                            hostfile.write(f"\n{redirect_ip} {site}")
            
            # --- Unblocking Logic: Outside Working Hours ---
            else:
                print(f"[{current_time.strftime('%H:%M:%S')}] ✅ FREE TIME: Websites unblocked.")
                
                # We read the file content entirely
                with open(DEFAULT_HOSTER, "r") as hostfile:
                    lines = hostfile.readlines()
                
                # Filter out the lines we added (the block entries)
                filtered_lines = []
                for line in lines:
                    # Keep the line only if it does NOT contain a site we want to block
                    # We also strip the line to remove blank/whitespace-only lines
                    if not any(site in line for site in sites_to_block) and line.strip():
                        filtered_lines.append(line)
                
                # Write the cleaned content back to the file
                with open(DEFAULT_HOSTER, "w") as hostfile:
                    hostfile.writelines(filtered_lines)
            
            # Wait for 5 minutes before checking again
            time.sleep(300) 

        except PermissionError:
            print(f"[{current_time.strftime('%H:%M:%S')}] ❌ ERROR: Permission denied. Please run the script as Administrator/root.")
            # Break out of the loop since without permission, it can't proceed
            break
        except Exception as e:
            print(f"[{current_time.strftime('%H:%M:%S')}] An unexpected error occurred: {e}")
            time.sleep(60) # Wait a bit before retrying

if __name__ == "__main__":
    # Call the function with the defined hours
    block_websites(START_HOUR, END_HOUR)