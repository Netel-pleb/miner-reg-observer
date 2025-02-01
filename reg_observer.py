import bittensor as bt
import requests
import json
import argparse
from datetime import timedelta
import time


webhook_url = "https://discord.com/api/webhooks/1335271704955715705/7z7JDnogM_EryjDhO5xGdVF9xsAWdGT0SAeNipGTxGyOXPhg0NtKgRt1SyOpGqVj2MAQ"

class ResisterObserver:
    def __init__(self, netuid, hotkeys, interval, duration):
        """
        Initialize the ResisterObserver class.
        Args:
            netuid (int): The netuid of the subnet to observe.
            hotkeys (list): A list of hotkeys to check in the metagraph.
            webhook_url (str): The Discord webhook URL for sending notifications.
            interval (int): The interval (in seconds) between checks.
            duration (int): The total runtime (in minutes) for the observer.
        """
        self.netuid = netuid
        self.hotkeys = hotkeys
        self.webhook_url = webhook_url
        self.interval = interval
        self.duration = duration

    def get_current_utc_time(self):
        """
        Get the current UTC time as a string.
        Returns:
            str: The current UTC time in the format "YYYY-MM-DD HH:MM:SS UTC".
        """
        return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    def generate_embed(self, hotkey, uid):
        """
        Generate a Discord embed-style dictionary for the webhook notification.
        Args:
            hotkey (str): The hotkey that was registered.
            uid (int): The UID of the hotkey in the metagraph.
        Returns:
            dict: A dictionary representing the embed content.
        """
        timestamp = self.get_current_utc_time()
        embed = {
            "title": "New Hotkey Registered in Subnet",
            "description": f"Hotkey `{hotkey}` has been registered in subnet `{self.netuid}`.",
            "fields": [
                {"name": "UID", "value": str(uid), "inline": True},
                {"name": "Timestamp", "value": timestamp, "inline": True}
            ],
            "color": 3066993  
        }
        return embed

    def webhook_raiser(self, hotkey, uid):
        """
        Send a webhook notification to Discord.
        Args:
            hotkey (str): The hotkey that was registered.
            uid (int): The UID of the hotkey in the metagraph.
        Returns:
            tuple: The response status code and text.
        """
        embed = self.generate_embed(hotkey, uid)
        data = {
            "embeds": [embed]
        }
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 204:
                print(f"[{self.get_current_utc_time()}] Webhook sent successfully for hotkey: {hotkey} in subnet {self.netuid}")
            else:
                print(f"[{self.get_current_utc_time()}] Failed to send webhook for hotkey: {hotkey}. Response: {response.status_code}, {response.text}")
            return response.status_code, response.text
        except Exception as e:
            print(f"[{self.get_current_utc_time()}] Error sending webhook for hotkey {hotkey}: {e}")
            return None, str(e)

    def check_metagraph(self):
        """
        Check the Bittensor subnet metagraph for the specified hotkeys.
        If a hotkey is found, send a webhook notification.
        """
        print(f"[{self.get_current_utc_time()}] Checking metagraph for netuid {self.netuid}...")
        try:
            metagraph = bt.subtensor(network="finney").metagraph(netuid=self.netuid)
            meta_hotkeys = metagraph.hotkeys
            print(meta_hotkeys)

            # Create a copy of the hotkeys list to iterate over
            for hotkey in self.hotkeys[:]:
                if hotkey in meta_hotkeys:
                    miner_uid = meta_hotkeys.index(hotkey)
                    print(f"[{self.get_current_utc_time()}] Hotkey {hotkey} is registered with UID {miner_uid}. Sending webhook...")
                    self.webhook_raiser(hotkey, miner_uid)
                    self.hotkeys.remove(hotkey)  # Remove the registered hotkey from the list
                else:
                    print(f"[{self.get_current_utc_time()}] Hotkey {hotkey} is NOT registered in the metagraph.")
        except Exception as e:
            print(f"[{self.get_current_utc_time()}] Error checking metagraph: {e}")

    def start_observing(self):
        """
        Start observing the subnet metagraph at regular intervals for a given duration.
        """
        print(f"[{self.get_current_utc_time()}] Starting observation on netuid {self.netuid} for hotkeys: {self.hotkeys}")
        end_time = time.time() + (self.duration * 60)

        while time.time() < end_time:
            if not self.hotkeys:  # Stop if all hotkeys are registered
                print(f"[{self.get_current_utc_time()}] All hotkeys are registered. Stopping observation.")
                break
            try:
                self.check_metagraph()
            except Exception as e:
                print(f"[{self.get_current_utc_time()}] Error during observation loop: {e}")
            print(f"[{self.get_current_utc_time()}] Sleeping for {self.interval} seconds...")
            time.sleep(self.interval)

        print(f"[{self.get_current_utc_time()}] Observation completed. Ran for {self.duration} minutes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Observe Bittensor subnet metagraph for hotkey registration.")
    parser.add_argument("--netuid", type=int, required=True, help="The netuid of the subnet to observe.")
    parser.add_argument("--hotkeys", type=str, required=True, help="Comma-separated list of hotkeys to observe.")
    parser.add_argument("--interval", type=int, default=20, help="Interval (in seconds) between checks. Default is 20 seconds.")
    parser.add_argument("--duration", type=int, default=30, help="Duration (in minutes) to run the observer. Default is 30 minutes.")
    args = parser.parse_args()

    # Convert hotkeys argument to a list
    hotkeys_list = [hk.strip() for hk in args.hotkeys.split(",")]

    # Initialize and start the observer
    observer = ResisterObserver(args.netuid, hotkeys_list, args.interval, args.duration)
    observer.start_observing()