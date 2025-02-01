# ResisterObserver

A Python script to monitor the registration of specific hotkeys in a Bittensor subnet's metagraph. Sends webhook notifications to Discord when a hotkey is detected as registered.

## Features
- Checks the registration status of specified hotkeys in a given subnet (netuid).
- Sends Discord notifications for newly registered hotkeys.
- Automatically stops the script once all hotkeys are registered.
- Skips checking already registered hotkeys in subsequent intervals.

## Prerequisites
- Python 3.6 or higher.
- Install the required dependencies:
  ```bash
  pip install bittensor requests
  ```

## Usage
Run the script from the command line with the following arguments:

### Required Arguments:
- `--netuid`: The netuid of the subnet to observe.
- `--hotkeys`: A comma-separated list of hotkeys to monitor.

### Optional Arguments:
- `--interval`: The interval (in seconds) between checks. Default is `20` seconds.
- `--duration`: The total runtime (in minutes) for the observer. Default is `120` minutes.

### Example Command:
```bash
python reg_observer.py --netuid 5 --hotkeys hotkey1,hotkey2,hotkey3 --interval 30 --duration 60
```

### Explanation:
- `--netuid 5`: Specifies the subnet with netuid `5` to monitor.
- `--hotkeys hotkey1,hotkey2,hotkey3`: Monitors the registration status of `hotkey1`, `hotkey2`, and `hotkey3`.
- `--interval 30`: Checks the metagraph every `30` seconds.
- `--duration 60`: Runs the observer for a maximum of `60` minutes unless all hotkeys are registered earlier.

## How It Works
1. The script initializes with the provided netuid and hotkeys.
2. It periodically checks the Bittensor metagraph for the registration status of the hotkeys.
3. When a hotkey is detected as registered:
   - A Discord webhook notification is sent.
   - The hotkey is removed from the monitoring list.
4. If all hotkeys are registered, the script stops automatically.

## Output
- Logs are printed to the terminal, showing the status of each hotkey and webhook notifications.
- Example output:
  ```plaintext
  [2025-02-01 15:05:00 UTC] Starting observation on netuid 5 for hotkeys: ['hotkey1', 'hotkey2']
  [2025-02-01 15:05:10 UTC] Hotkey hotkey1 is registered with UID 42. Sending webhook...
  [2025-02-01 15:05:12 UTC] Webhook sent successfully for hotkey: hotkey1 in subnet 5
  [2025-02-01 15:05:15 UTC] Hotkey hotkey2 is NOT registered in the metagraph.
  [2025-02-01 15:05:20 UTC] All hotkeys are registered. Stopping observation.
  ```

## Notes
- Make sure the Discord webhook URL is updated in the script before running.
- The script stops automatically when all hotkeys are registered or the duration ends.
- Current webhook url in the repo is fake url. You need to change it to yours

## License
This project is licensed under the MIT License.